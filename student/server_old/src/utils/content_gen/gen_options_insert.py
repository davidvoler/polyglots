from utils.db_sync import get_query_results, run_query, get_pg_con, close_pg_con
from utils.content_gen.context import remove_punct
import random
from datetime import datetime
import psycopg
import time

def options_remove_duplicates(options:list):
    seen_normalized = set()
    unique_option = []
    for o in options:
        normalized = remove_punct(o.lower().strip())
        if normalized not in seen_normalized:
            seen_normalized.add(normalized)
            unique_option.append(o)
    return unique_option


def get_options_all(lang:str,min_count:int, max_count:int):
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
    results =  get_query_results(sql, params)
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
    params = []
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
        params.append((lang, r.get("id"), r.get("sentence"), r.get("words", []), r.get("root"), options[:6], r.get("w_count")))
        if len(params) > 500:
            # run_sql_batch(params)
            run_sql_batch(params)
            # print(f"{datetime.now()}: Updated {len(params)} sentences for {lang} with word count between {min_count} and {max_count}")
            params = []
    run_sql_batch(params)
    


def run_sql_batch(params:list):
    # conn = psycopg.connect("postgresql://polyglots:polyglots@localhost:5432/polyglots",
    #                        autocommit=False,  # Manual transaction control
    #                        prepare_threshold=5)
        
    conn = get_pg_con()
    # with conn:
    with conn.cursor() as cursor:
        cursor.execute("BEGIN")
        sql = f"""
                INSERT INTO tatoeba.parts
                (lang, part_id, text, words, root, options, w_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
        """
        cursor.executemany(
                sql, params)
        cursor.execute("COMMIT")


def run_batch(sql, params:list):
    conn = get_pg_con()
    # with conn:
    with conn.cursor() as cursor:
        cursor.execute("BEGIN")
        cursor.executemany(
                sql, params)
        cursor.execute("COMMIT")

def gen_options_simple(lang:str, w_count:int):
    print(f"{datetime.now()}  Generating simple options for {lang} with word count {w_count}")
    sentences = []
    sql = """
        SELECT * FROM tatoeba.prepared_sentences
        WHERE lang = %s
        AND w_count = %s
    """
    results = get_query_results(sql, (lang, w_count))
    for r in results:
        sentences.append(r)
    # Randomly select up to 6 sentences
    if len(sentences) == 0:
        return 
    print(f"Found {len(sentences)} sentences for {lang} with word count {w_count}")
    
    params = []
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
        options = options[:6]  # Limit to 6 options
        params.append((lang, _id, s.get("sentence"), s.get("words", []), s.get("root"), options, s.get("w_count")))
        if len(params) >= 500:
            run_sql_batch(params)
            print(f"{datetime.now()}: Updated {len(params)} sentences for {lang} with word count {w_count}")
            params = []
    run_sql_batch(params)
                 
def gen_options(lang:str):
    for i in range(1, 3):
        gen_options_simple(lang, i)
    get_options_all(lang, 3, 3)
    get_options_all(lang, 4, 4)
    get_options_all(lang, 5, 5)
    get_options_all(lang, 6, 7)
    get_options_all(lang, 8, 9)
    get_options_all(lang, 10, 13)
    get_options_all(lang, 14, 18)
    get_options_all(lang, 19, 40)






def gen_options_all_langs():
    sql = """
        SELECT DISTINCT lang FROM tatoeba.prepared_sentences
        """
    results = get_query_results(sql,None)
    for r in results:
        gen_options(r.get("lang"))
        # gen_options_all_async(r.get("lang"))



def save_links():
    sql = """
        SELECT distinct lang FROM tatoeba.prepared_sentences
    """
    results = get_query_results(sql, None)
    langs = [r.get("lang") for r in results]
    sql = """
         SELECT distinct lang FROM tatoeba.links2
    """
    results = get_query_results(sql, (langs[0],))
    links_langs =  [r.get("lang") for r in results]
    
    for lang in langs:
        if lang in links_langs:
            print(f"Links for {lang} already exist, skipping")
            continue
        print(f"{datetime.now()}  Saving links for {lang}")
        sql = """
            insert into tatoeba.links2(id, lang, trans_id)
            SELECT 
                s1.part_id as id,
                s1.lang as lang,
                l.trans_id as trans_id
            FROM tatoeba.parts s1
            JOIN tatoeba.links l 
                ON s1.part_id = l.id
            where  s1.lang=%s
        """
        run_query(sql, (lang,))


def save_links2():
    sql = """
        SELECT distinct lang FROM tatoeba.prepared_sentences
    """
    results = get_query_results(sql, None)
    langs = [r.get("lang") for r in results]
    sql = """
         SELECT distinct lang FROM tatoeba.links3
    """
    results = get_query_results(sql, (langs[0],))
    links_langs =  [r.get("lang") for r in results]
    for lang in langs:
        if lang in links_langs:
            print(f"Links for {lang} already exist, skipping")
            continue
        print(f"{datetime.now()}  Saving links for {lang}")
        sql = """
            insert into tatoeba.links3(lang, to_lang, id,  trans_id)
            SELECT 
                l.lang as lang,
                s.lang as to_lang,
                l.trans_id as trans_id,
                l.id as id
            FROM tatoeba.links2 l
            JOIN tatoeba.parts s 
                ON s.part_id = l.trans_id
            where  s.lang=%s
        """
        run_query(sql, (lang,))

def words_lists():
    sql = """
        SELECT distinct lang FROM tatoeba.parts
    """
    results = get_query_results(sql, None)
    langs = [r.get("lang") for r in results]
    for lang in langs:
        all_words = {}
        sql = """
            SELECT * FROM tatoeba.parts
            WHERE lang = %s
        """
        results = get_query_results(sql, (lang,))
        for r in results:
            words = r.get("words", [])
            part_id = r.get("part_id")
            # print(f"Processing part {part_id} for {lang} {words}")
            if not words:
                continue
            for word in words:
                if word not in all_words.keys():
                    all_words[word] = []
                all_words[word].append(part_id)
        
        sql = """
            INSERT INTO tatoeba.words(lang, word, ids, ids_count) VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        params = []
        for k, v  in all_words.items():
            params.append((lang, k, v, len(v)))
        print(f"Saving {len(params)} words for {lang}")
        run_batch(sql, params)



def step_words_by_len():
    sql = """
        SELECT distinct lang FROM tatoeba.parts
    """
    results = get_query_results(sql, None)
    langs = [r.get("lang") for r in results]
    for lang in langs:
        all_words = {}
        sql = """
            SELECT * FROM tatoeba.parts
            WHERE lang = %s
        """
        results = get_query_results(sql, (lang,))
        for r in results:
            words = r.get("words", [])
            part_id = r.get("part_id")
            w_count = r.get("w_count", 0)
            # print(f"Processing part {part_id} for {lang} {words}")
            if not words:
                continue
            for word in words:
                if word not in all_words.keys():
                    all_words[word] = []
                all_words[word].append((w_count, part_id))
        
        

        sql = """
            INSERT INTO tatoeba.words2(lang, word,ids,ids_count) VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        params = []
        for k, v  in all_words.items():
            w_sorted = []
            v.sort(key=lambda x: x[0])
            for w in v:
                w_sorted.append(w[1])
            params.append((lang, k, w_sorted, len(w_sorted)))
        print(f"Saving {len(params)} words for {lang}")
        run_batch(sql, params)




def create_words_step(lang, word:str, ids:list, step:int):
    if step < 30:
        order = "order by w_count  asc"
        limit = 20
    elif step < 50:
        order = "order by w_count asc"
        limit = 25
    elif step < 100:
        order = "order by w_count asc"
        limit = 30
    elif step  < 200:
        order = ""
        limit = 40
    else:
        order = ""
        limit = 60
    safe_word =str(word).replace("'", "''")
    sql = f"""
        select * from tatoeba.parts
        where lang = '{lang}' 
        and words @> '{{"{safe_word}"}}'
        {order} 
        limit {limit}
    """
    params = (lang, None)
    results = get_query_results(sql, None)
    nids = [r.get("part_id") for r in results]
    if len(nids) == 0:
        # print(f"No parts found for {lang} with word {word} in step {step}")
        return
    sql = """
        INSERT INTO tatoeba.steps(lang, step, word, ids, ids_count)
        values (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    # print (f"Creating step {step} for {lang} with word {word} and {len(nids)} ids")
    run_query(sql, (lang, step, word, nids, len(nids)))

    

def generate_steps():
    print(f"{datetime.now()}  Generating steps for all languages")
    """
    Generate steps for each language.
    """
    sql = """
        SELECT distinct lang FROM tatoeba.parts
    """
    results = get_query_results(sql, None)
    langs = [r.get("lang") for r in results]
    print(f"Found {len(langs)} languages to generate steps for")
    for lang in langs:
        print(f"{datetime.now()}: Generated steps for {lang}")
        sql = """
            SELECT *  FROM tatoeba.words2 
            where lang = %s
            and ids_count > 6
            order by ids_count desc
        """
        results = get_query_results(sql, (lang,))
        step = 0
        params = []
        for r in results:
            word = r.get("word")
            ids = r.get("ids", [])
            if not ids or len(ids) == 0:
                continue
            step+=1
            if step < 300:
                ids = ids[:300]
            else:
                pass
            params.append((lang, step, word, ids, len(ids)))
        insert_sql = """
            INSERT INTO tatoeba.steps(lang, step, word, ids, ids_count)
            values (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        if len(params) > 0:
            run_batch(insert_sql, params)
            print(f"{datetime.now()}: Processed {len(params)} words for {lang} in steps")



def generate_steps3():
    print(f"{datetime.now()}  Generating steps for all languages")
    """
    Generate steps for each language.
    """
    sql = """
        SELECT distinct lang FROM tatoeba.parts
    """
    results = get_query_results(sql, None)
    langs = [r.get("lang") for r in results]
    print(f"Found {len(langs)} languages to generate steps for")
    for lang in langs:
        print(f"{datetime.now()}: Generated steps for {lang}")
        sql = """
            SELECT *  FROM tatoeba.steps2 
            where lang = %s
            order by step
        """
        results = get_query_results(sql, (lang,))
        step = 0
        params = []
        last_words = []
        last_ids = []
        for r in results:
            word = r.get("word")
            ids = r.get("ids", [])
            if not ids or len(ids) == 0:
                continue
            step+=1
            if step % 100 == 0:
                print(f"{datetime.now()}: Processed {step} words for {lang}")
            last_ids += ids
            last_words.append(word)
            if len(last_ids) > 25:
                params.append((lang, step, last_words, len(last_words), last_ids, len(last_ids)))
                last_words = []
                last_ids = []
        insert_sql = """
            INSERT INTO tatoeba.steps3(lang, step, words, words_count, ids, ids_count)
            values (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        if len(last_ids) > 0:
            params.append((lang, step, last_words, len(last_words), last_ids, len(last_ids)))
        if len(params) > 0:
            run_batch(insert_sql, params)
            print(f"{datetime.now()}: Processed {len(params)} words for {lang} in steps")




def test_in_words():
    """
    Test the in operator with words.
    """
    sql = """
        SELECT * FROM tatoeba.parts
        WHERE lang = %s
        and words @> '{"apologised"}'
        
    """
    params = ('eng',)
    results = get_query_results(sql, params)
    for r in results:
        print(r)


T_LANGS = [
'ara',
'asm',
'aze',
'bel',
'ben',
'ber',
'bre',
'bul',
'cat',
'ces',
'ckb',
'cmn',
'dan',
'deu',
'ell',
'eng',
'epo',
'est',
'eus',
'fin',
'fra',
'glg',
'gos',
'hau',
'heb',
'hin',
'hrv',
'hun',
'hye',
'ido',
'ile',
'ina',
'ind',
'isl',
'ita',
'jbo',
'jpn',
'kab',
'kat',
'kmr',
'kor',
'kzj',
'lat',
'lfn',
'lit',
'lvs',
'mar',
'mkd',
'nds',
'nld',
'nnb',
'nno',
'nob',
'oci',
'oss',
'pes',
'pol',
'por',
'ron',
'run',
'rus',
'sat',
'shi',
'slk',
'slv',
'spa',
'srp',
'swc',
'swe',
'tat',
'tgl',
'tha',
'tig',
'tlh',
'tok',
'tuk',
'tur',
'uig',
'ukr',
'vie',
'vol',
'yid',
'yue',
'zgh',
'zsm',
]


def step_lang_to_lang():
    sql = """
    SELECT lang, to_lang, count(id) as ids_count
    FROM tatoeba.links4
    WHERE lang=%s
    GROUP by lang, to_lang
    """
    langs_comb = []
    min_links = 800
    lang_to_lang = 0    
    for lang in T_LANGS:
        data = get_query_results(sql, (lang,))
        for d in data:
            id_count = d.get("ids_count")
            lang = d.get("lang")
            to_lang = d.get("to_lang")
            if lang == to_lang:
                continue
            if id_count and id_count > min_links:
                print(d)
                lang_to_lang+=1
                langs_comb.append((lang, to_lang, id_count))
            # else:
                # print("not enough links ")
    sql = """
    insert into tatoeba.lang_info
    (lang, to_lang, link_count)
    VALUES(%s, %s, %s)    
    """
    for cmb in langs_comb:
        run_query(sql, cmb)
    print (f'number of language pairs for min links { min_links} is: {lang_to_lang}')


def _get_step_per_lang(lang, to_lang, ids:list, step:int, word):
    placeholders = ', '.join(['%s'] * len(ids))  
    # Adjust the number of placeholders as needed
    sql = f"""
        SELECT * from tatoeba.links4 
        WHERE lang = %s 
        AND to_lang = %s
        and id in ({placeholders})
    """
    params = [lang, to_lang] + ids
    results = get_query_results(sql, params)
    l_ids= []
    for r in results:
        l_ids.append(r.get("id"))
    if len(l_ids) <4:
        return 
    sql = """
        INSERT INTO tatoeba.steps4(lang, to_lang, step, ids, ids_count, word)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    

    params = (lang, to_lang, step, l_ids, len(l_ids), word)
    # print(sql, params)
    run_query(sql, params)



def create_step_lang_per_lang():
    for lang in T_LANGS:
        t = time.time()
        sql = """
            SELECT * from tatoeba.steps
            WHERE lang = %s
            AND to_lang = %s
        """
        data = get_query_results(sql,(lang,))
        sql = """
            SELECT to_lang FROM tatoeba.lang_info
            WHERE lang = %s
        """
        res = get_query_results(sql,(lang,))
        to_langs = [r.get("to_lang") for r in res]
        for d in data:
            ids = d.get("ids")
            step = d.get("step")
            word = d.get("word")
            for to_lang in to_langs:
                _get_step_per_lang(lang, to_lang, ids, step, word)
        print(f"{datetime.now()} {lang}  {int(time.time() - t) }")

    



def order_steps_lang_to_lang():
    t = time.time()
    select_sql = """
        SELECT * FROM tatoeba.steps4
        WHERE lang = %s
        AND to_lang = %s
        ORDER by step
    """
    insert_sql = """
        INSERT INTO tatoeba.steps5(lang, to_lang, step, ids, ids_count, word)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    info_sql = """
        insert into  tatoeba.lang_info1 (lang, to_lang, words, min_step, max_step)
        VALUES (%s, %s, %s, %s,%s)
    """
    lang_info_sql = """
        select * from tatoeba.lang_info
    """
    langs_data = get_query_results(lang_info_sql,None)
    for l in langs_data:
        lang = l.get('lang')
        to_lang = l.get('to_lang')
        t= time.time()
        step = 0
        data = get_query_results(select_sql, (lang, to_lang,))
        for d in data:
            step += 1
            run_query(insert_sql, 
                        (lang, to_lang, step, 
                        d.get('ids'), 
                        d.get("ids_count"),
                        d.get('word'))
                        )
        run_query(info_sql, (lang, to_lang, step,1,step))
        print (f"{lang} {to_lang} took {time.time() -t} seconds")


        
        
