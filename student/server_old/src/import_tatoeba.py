import csv
from utils.db import run_query, get_query_results
import asyncio
import pycountry
import langcodes
from babel import Locale
from utils.content_gen.context import get_words_all_structure, split_words_simple, remove_punct
from utils.content_gen.gen_options import gen_options, gen_options_all_langs, get_options_all
# Convert 3-letter to 2-letter


async def import_tatoeba_sentences():
    with open('/Users/davidle/Downloads/sentences.csv', 'r', encoding='utf-8') as file:
        tsv_reader = csv.DictReader(file, delimiter='\t', fieldnames=['id', 'lang', 'text'])
        i = 0
        errors = 0
        for row in tsv_reader:
            _id = int(row['id'].strip())
            if _id < 6114068:
                continue
            print(row)  # Each row is a dictionary
            sql = """
            INSERT INTO tatoeba.sentences (id, lang, text)
            VALUES (%s, %s, %s)"""
            params = (int(row['id'].strip()), row['lang'].strip(), row['text'].strip())
            print (f"Inserting row {i}: {params}")
            try:
                await run_query(sql, params)
                i += 1
            except Exception as e:
                print(f"Error inserting row {i}: {e}")
                errors += 1
                continue
            # Access columns: row['column_name']
        print(f"Inserted {i} rows into the database.")


async def import_tatoeba_links():
    with open('/Users/davidle/Downloads/links.csv', 'r', encoding='utf-8') as file:
        tsv_reader = csv.DictReader(file, delimiter='\t', fieldnames=['id', 'trans_id'])
        i = 0
        errors = 0
        for row in tsv_reader:
            
            sql = """
            INSERT INTO tatoeba.links (id, translation_id)
            VALUES (%s, %s)"""
            params = (int(row['id'].strip()),int(row['trans_id'].strip()))
            print (f"Inserting row {i}: {params}")
            try:
                await run_query(sql, params)
                i += 1
            except Exception as e:
                print(f"Error inserting row {i}: {e}")
                errors += 1
                continue
            # Access columns: row['column_name']
        print(f"Inserted {i} rows into the database.")




async def remove_short_sentences():
    sql = """
    select  lang, count(*) as  c from tatoeba.sentences 
    group by 1
    order by c desc
    """
    results = await get_query_results(sql, None)
    for r in results:
        # if r.get('c') <5000:
        #     continue
        lang = pycountry.languages.get(alpha_3=r.get('lang'))
        code = ''
        name = ''
        try:
            code = lang.alpha_2
        except:
            pass
        try:
            name = lang.name
        except:
            pass
        print(f"Language: {r.get('lang')} - {code} - {name} - {r.get('c')}")
        sql = """
        INSERT INTO tatoeba.info (lang3, lang2, name, count)
        VALUES (%s, %s, %s, %s)"""
        params = (r.get('lang'), code, name, r.get('c'))
        try:
            await run_query(sql, params)
        except Exception as e:
            print(f"Error inserting language info: {e}")
            continue

async def select_all_sentences(cnt:int = 5000):
    sql = """
    SELECT * FROM tatoeba.info
    WHERE "count" > %s
    """
    results = await get_query_results(sql, (cnt,))
    for r in results:
        print(r)
    


async def exists_or_duplicated(lang:str, id, text:str):
    sql = """
    SELECT * FROM tatoeba.prepared_sentences
    WHERE lang = %s AND id = %s
    """
    params = (lang, id)
    results = await get_query_results(sql, params)
    if len(results) > 0:
        return True
    return False
    # sql = """
    # SELECT * FROM tatoeba.prepared_sentences
    # WHERE lang = %s AND sentence = %s
    # """
    # params = (lang, text)
    # results = await get_query_results(sql, params)
    # if results:
    #     return True
    # return False

async def get_offset(lang:str):
    sql = """
    SELECT count(id) as count_id FROM tatoeba.prepared_sentences
    WHERE lang = %s
    """
    params = (lang,)
    results = await get_query_results(sql, params)
    print(f"Results for {lang}: {results}")
    if results and results[0].get('count_id'):
        return results[0].get('count_id')
    return 0

async def short_sentences(lang:str, limit_sentence_len:int = 120):
    long_count = 0
    short_count = 0
    offset = await get_offset(lang)
    print(f"Offset for {lang}: {offset}")
    sql = """
    SELECT * FROM tatoeba.sentences
    WHERE lang = %s
    offset %s
    """
    results = await get_query_results(sql, (lang,offset))
    for r in results:
        text = r.get('text').strip()
        if not text:
            continue
        if len(text) > limit_sentence_len:
            long_count += 1
            continue
        # if await exists_or_duplicated(lang, r.get('id'), text):
        #     print(f"Sentence already exists or is duplicated: {text}")
        #     continue
        short_count += 1

        words, all_words, pos, root, propn, stop_words = get_words_all_structure(r.get('text'), lang)
        first_c = text[:int(len(text)/4)]
        last_c = text[-1*(int(len(text)/4)):]
        sql = """
        INSERT INTO tatoeba.prepared_sentences (id, lang, sentence, all_words, c_count, first, first_c, last_c, pos, propn, root, stop_words, w_count, words)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            first = all_words[0] 
        except:
            first = ''
        params = (r.get('id'), r.get('lang'), text, all_words, len(text), first, first_c, last_c, pos, propn, root, stop_words, len(all_words), words)
        try:
            await run_query(sql, params)
        except Exception as e:
            print(f"Error inserting short sentence: {e}")
            continue
    print(f"Long sentences: {long_count}, Short sentences: {short_count}")

def get_sentence_words(sentence:str, lang:str):
    """
    Get words from a sentence, removing punctuation and converting to lowercase.
    """
    words = sentence.split()
    results = []
    for w in words:
        w = remove_punct(w.strip())
        if w:
            results.append(w)
    return results

async def short_sentences_no_nlp(lang:str, limit_sentence_len:int = 120):
    long_count = 0
    short_count = 0
    offset = await get_offset(lang)
    print(f"Offset for {lang}: {offset}")
    sql = """
    SELECT * FROM tatoeba.sentences
    WHERE lang = %s
    offset %s
    """
    results = await get_query_results(sql, (lang,offset))
    for r in results:
        text = r.get('text').strip()
        if not text:
            continue
        if len(text) > limit_sentence_len:
            long_count += 1
            continue
        # if await exists_or_duplicated(lang, r.get('id'), text):
        #     print(f"Sentence already exists or is duplicated: {text}")
        #     continue
        short_count += 1
        words = get_sentence_words(text, lang)
        first_c = text[:int(len(text)/4)]
        last_c = text[-1*(int(len(text)/4)):]
        sql = """
        INSERT INTO tatoeba.prepared_sentences (id, lang, sentence, all_words, c_count, first, first_c, last_c, w_count, words)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            first = words[0] 
        except:
            first = ''
        params = (r.get('id'), lang, text, words, len(text), first, first_c, last_c, len(words), words)
        try:
            await run_query(sql, params)
        except Exception as e:
            print(f"Error inserting short sentence: {e}")
            continue
    print(f"Long sentences: {long_count}, Short sentences: {short_count}")



NLP_LANGS = [
    'ca', 'zh', 'hr', 'da', 'nl', 'en', 'fi', 'fr', 
    'el', 'it', 'ja', 'ko', 'lt', 'mk', 'nb', 'pl', 
    'pt', 'ro', 'ru', 'sl', 'es', 'sv', 'uk', 'de'] 


async def import_all_non_nlp_sentences():
    sql = """
    SELECT * FROM tatoeba.info 
        where count > 5000
    """
    results = await get_query_results(sql, None)
    for r in results:
        lang2 = r.get('lang2').strip()
        lang3 = r.get('lang3').strip()
        if not lang2:
            print(f"Skipping language {lang3} as it has no 2-letter code.")
            continue
        if lang2 in NLP_LANGS:
            print(f"Skipping {lang2} as it is an NLP language.")
            continue
        if lang3 in ['ara', 'heb']:
            continue
        print(f"Importing sentences for {lang3}")
        await short_sentences_no_nlp(lang3, 120)
        
         
async def import_all_nlp_sentences():
    sql = """
    SELECT * FROM tatoeba.info 
        where count > 5000
    """
    tasks = []
    results = await get_query_results(sql, None)
    for r in results:
        lang2 = r.get('lang2').strip()
        lang3 = r.get('lang3').strip()
        if not lang2:
            print(f"Skipping language {lang3} as it has no 2-letter code.")
            continue
        if lang2 in NLP_LANGS:
            if lang3 in ['eng', 'cmn', 'jpn', 'ell', 'ita']:
                continue
            print(f"Importing sentences for {lang3}")
            await short_sentences(lang3, 120)

async def import_missing_l2_sentences():
    sql = """
    SELECT * FROM tatoeba.info 
        where count > 5000
    """
    results = await get_query_results(sql, None)
    for r in results:
        lang2 = r.get('lang2').strip()
        lang3 = r.get('lang3').strip()
        if not lang2:
            print(f"Importing sentences for {lang3}")
            await short_sentences_no_nlp(lang3, 120)
        
# asyncio.run(import_tatoeba_sentences())
# asyncio.run(import_tatoeba_links())
# asyncio.run(remove_short_sentences())
# asyncio.run(select_all_sentences(5000))
# asyncio.run(short_sentences('eng'))
# asyncio.run(short_sentences('jpn', 60))
# asyncio.run(short_sentences('fra', 135))
# asyncio.run(short_sentences('deu', 130))
# asyncio.run(short_sentences('por', 130))
# asyncio.run(short_sentences('fra', 130))
# asyncio.run(short_sentences('fin', 130))
# asyncio.run(short_sentences('nld', 130))
# asyncio.run(short_sentences('ukr', 130))
# asyncio.run(short_sentences('rus', 130))
# asyncio.run(short_sentences('dan', 130))
# asyncio.run(short_sentences('swe', 130))
# asyncio.run(short_sentences('ron', 130))
# asyncio.run(short_sentences('kor', 130))
# asyncio.run(short_sentences('pol', 130))
# asyncio.run(short_sentences('nob', 130))
# asyncio.run(short_sentences('cat', 130))
# asyncio.run(short_sentences('hrv', 130))
# asyncio.run(short_sentences('lit', 130))
# asyncio.run(short_sentences('slv', 130))
# asyncio.run(short_sentences('mkd', 130))
# asyncio.run(short_sentences('spa', 130))
# asyncio.run(short_sentences('ell', 130))
# asyncio.run(import_missing_l2_sentences())
# asyncio.run(import_all_nlp_sentences())

# asyncio.run(gen_options_all_langs())
# asyncio.run(gen_options_all_langs())

# from utils.content_gen.gen_options_sync import gen_options_simple, get_options_all, gen_options_all_langs

# gen_options_simple('fra', 2)
# get_options_all('dan', 3, 3)
# gen_options_all_langs()

            
from utils.content_gen.gen_options_insert import (gen_options_simple, get_options_all, gen_options_all_langs, 
                                                  save_links, save_links2, words_lists, test_in_words,
                                                  generate_steps,
                                                  step_lang_to_lang,
                                                  )
# gen_options_simple('ara', 1)
# get_options_all('ara', 3, 3)
# gen_options_all_langs()
# save_links2()
# words_lists()
# test_in_words()
# generate_steps()
step_lang_to_lang()