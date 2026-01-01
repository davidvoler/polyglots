from utils.db import get_query_results, run_query
from utils.content_gen.context import remove_punct
import random
import asyncio
from datetime import datetime

def options_remove_duplicates(options:list):
    seen_normalized = set()
    unique_option = []
    for o in options:
        normalized = remove_punct(o.lower().strip())
        if normalized not in seen_normalized:
            seen_normalized.add(normalized)
            unique_option.append(o)
    return unique_option


async def get_options_all(lang:str,min_count:int, max_count:int):
    print(f"{datetime.now()} Generating options for {lang} with word count between {min_count} and {max_count}")
    sentences  = []
    sentences_by_random = []
    by_words = {}
    by_propn = {}
    by_root = {}
    by_first = {}
    by_last = {}
    by_last_c = {}
    by_pos = {}
    """
    Generate options based on a list of words.
    """
    sql = f"""
        SELECT * FROM tatoeba.prepared_sentences
        WHERE lang = %s
        AND w_count >= %s 
        AND w_count <= %s;
    """
    params = tuple([lang, min_count, max_count])
    results =  await get_query_results(sql, params)
    for r in results:
        _id = r.get("id")
        sentences.append(r)
        sentence = r.get("sentence", "")
        if not sentence:
            continue
        sentences_by_random.append(sentence)
        words =  r.get("words", [])
        if len(words) < 2:
            words = r.get("all_words", [])
        sample_size = min(2, len(words))
        words2 = random.sample(words,sample_size)
        words2.sort()
        words2_key = "_".join(words2)
        l = by_words.get(words2_key, [])
        l.append(sentence)
        by_words[words2_key] = l
        root = r.get("root", [])
        if root:
            l = by_root.get(root, [])
            l.append(sentence)
            by_root[root] = l
        first = r.get("first", [])
        if first:
            l = by_first.get(first, [])
            l.append(sentence)
            by_first[first] = l
        last_c = r.get("last_c", [])
        if last_c:
            l = by_last_c.get(last_c, [])
            l.append(sentence)
            by_last_c[last_c] = l
        pos = r.get("pos", [])
        if pos:
            pos_key = "_".join(pos[:3])
            l = by_pos.get(pos_key, [])
            l.append(sentence)
            by_pos[pos_key] = l
        propn = r.get("propn", [])
        if propn and len(propn) > 0:
            propn_key = random.choice(propn)
            l = by_propn.get(propn_key, [])
            l.append(sentence)
            by_propn[propn_key] = l
        first_c = r.get("first_c", [])
        if first_c:
            l = by_last.get(first_c, [])
            l.append(sentence)
            by_last[first_c] = l
        last = r.get("last", [])
        if last:
            l = by_last.get(last, [])
            l.append(sentence)
            by_last[last] = l

    # for k in by_words.keys():
    #     by_words[k] = list(set(by_words[k]))
    # for k in by_propn.keys():
    #     by_propn[k] = list(set(by_propn[k]))
    # for k in by_root.keys():
    #     by_root[k] = list(set(by_root[k]))
    # for k in by_first.keys():
    #     by_first[k] = list(set(by_first[k]))
    # for k in by_last_c.keys():
    #     by_last_c[k] = list(set(by_last_c[k]))
    # for k in by_pos.keys():
    #     by_pos[k] = list(set(by_pos[k]))
    # sentences_by_random = list(set(sentences_by_random))
    
    for r in sentences:
        options = []
        propn = r.get("propn", [])
        root = r.get("root", '')
        first = r.get("first", '')
        last_c = r.get("last_c", [])
        first_c = r.get("first_c", [])
        last = r.get("last", '')
        pos = r.get("pos", [])

        words =  r.get("words", [])
        if len(words) < 2:
            words = r.get("all_words", [])
        sample_size = min(2, len(words))
        words2 = random.sample(words,sample_size)
        words2.sort()
        words2_key = "_".join(words2)
        l = by_words.get(words2_key, [])
        if len(l) > 0:
            sample_size  = min(3, len(l))
            options +=  random.sample(l,sample_size)
        l = by_first.get(first, [])
        if len(l) > 0:
            sample_size  = min(3, len(l))
            options += random.sample(l,sample_size)
        if root:
            l = by_root.get(root, [])
            sample_size  = min(3, len(l))
            if len(l) > 0:
                options +=  random.sample(l,sample_size)
        if propn and  len(propn) > 0:
            propn_key = random.choice(propn)
            l = by_propn.get(propn_key, [])
            if len(l) > 0:
                sample_size  = min(2, len(l))
                options += random.sample(l,sample_size)
        l = by_last_c.get(last_c, [])
        if len(l) > 0:
            sample_size  = min(3, len(l))
            options +=  random.sample(l,sample_size)
        if pos and len(pos) > 0:
            pos_key = "_".join(pos[:3])
            l = by_pos.get(pos_key, [])
            if len(l) > 0:
                sample_size = min(3, len(l))
                options +=  random.sample(l,sample_size)

        if len(options) < 7:
            sample_size = min(7 - len(options), len(sentences_by_random))
            options += random.sample(sentences_by_random,sample_size)
        options = options_remove_duplicates([r.get("sentence")]+options)
        random.shuffle(options)
        try:
            options.remove(r.get("sentence"))
        except:
            pass
        sql = """
            UPDATE tatoeba.prepared_sentences
            SET options = %s
            WHERE id = %s
        """
        await run_query(sql, (options[:6], r.get("id")))
    # Get sentences by last word





async def gen_options_simple(lang:str, w_count:int):
    print(f"{datetime.now()}  Generating simple options for {lang} with word count {w_count}")
    sentences = []
    sql = """
        SELECT * FROM tatoeba.prepared_sentences
        WHERE lang = %s
        AND w_count = %s
    """
    results = await get_query_results(sql, (lang, w_count))
    for r in results:
        sentences.append(r)
    # Randomly select up to 6 sentences
    if len(sentences) == 0:
        return 
    for s in sentences:
        options = []
        for i in range(6):
            o = random.choice(sentences)
            options.append(o.get("sentence"))
        
        options = list(set(options))  # Remove duplicates
        options = options_remove_duplicates([s.get("sentence")]+options)
        try:
            options.remove(s.get("sentence"))
        except:
            pass
        # update database with options
        _id = s.get("id")
        o_count = len(options)
        sql = f"""
            UPDATE tatoeba.prepared_sentences
            SET "options" = %s 
            WHERE id= %s
        """
        
        await run_query(sql, (options, _id))    


async def gen_options(lang:str):
    for i in range(1, 3):
        await gen_options_simple(lang, i)
    await get_options_all(lang, 3, 3)
    await get_options_all(lang, 4, 4)
    await get_options_all(lang, 5, 5)
    await get_options_all(lang, 6, 7)
    await get_options_all(lang, 8, 9)
    await get_options_all(lang, 10, 13)
    await get_options_all(lang, 14, 18)
    await get_options_all(lang, 19, 40)



async def gen_options_all_async(lang:str):
    task = []
    for i in range(1, 3):
        task.append(gen_options_simple(lang, i))
    task.append(get_options_all(lang, 3, 3))
    task.append(get_options_all(lang, 4, 4))
    task.append(get_options_all(lang, 5, 5))
    task.append(get_options_all(lang, 6, 7))
    task.append(get_options_all(lang, 8, 9))
    task.append(get_options_all(lang, 10, 13))
    task.append(get_options_all(lang, 14, 18))
    task.append(get_options_all(lang, 19, 40))
    await asyncio.gather(*task)


async def gen_options_all_langs():
    sql = """
        SELECT DISTINCT lang FROM tatoeba.prepared_sentences
        """
    results = await get_query_results(sql,None)
    for r in results:
        await gen_options(r.get("lang"))
        # await gen_options_all_async(r.get("lang"))
