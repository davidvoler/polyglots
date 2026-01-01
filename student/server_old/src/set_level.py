from utils.content_gen.words import rank_words
from utils.db import get_pg_con
# from utils.quiz.quiz_query import get_quiz
from export.export import *
SCHEMA = "polyglots_quiz"
CONTENT_SCHEMA = "polyglots_content"
USER_SCHEMA = "polyglots_users"
USER_ID = "aaa"

LANGS = ['ar',
'cs',
'de',
'el',
'en',
'es',
'fr',
'he',
'hi',
'it',
'ja',
'pt',
'pt-PT',
'ru',
'zh-Hans']

LAST_PART_LANGS = ['ja', 'de']

async def set_parts_rank():
    conn = await get_pg_con()
    sql = f"""SELECT part_id, lang, words FROM {SCHEMA}.parts"""
    cursor = conn.cursor()
    await cursor.execute(sql)
    results = await cursor.fetchall()
    for r in results:
        part_id = r.get("part_id")
        lang = r.get("lang")
        words = r.get("words")
        max_r = 0
        # print (f"part_id:{part_id} lang: {lang}, words: {words}")
        for w in words:
            rnk = rank_words(lang, w)
            max_r = max(max_r, rnk)
        update_sql = f"""UPDATE  {SCHEMA}.parts set level =%s where part_id=%s and lang=%s""" 
        # print(update_sql)
        await cursor.execute(update_sql, (max_r, part_id,lang))
        # await conn.commit()
        # 

async def create_words_list():

    conn = await get_pg_con()
    for l in LANGS:
        all_words =  set()
        sql = f"""SELECT part_id, lang, words FROM {SCHEMA}.parts WHERE lang=%s"""
    
        cursor = conn.cursor()
        await cursor.execute(sql, (l,))
        results = await cursor.fetchall()
        for r in results:
            words = r.get("words")
            for w in words:
                all_words.add(w)
        # save the words to database
        for w in all_words:
            rank = rank_words(l, w)
            sql = f"""INSERT INTO {SCHEMA}.words (word_id, lang, word, level) VALUES (%s, %s, %s, %s)"""
            try:
                await cursor.execute(sql, (w, l, w, rank))
            except Exception as e:
                print(f"Error executing SQL: {sql}")
                print(e)        


def get_group_size_orig(step):
    if step <= 10:
        return 4
    elif step <= 20:
        return 5
    elif step <= 30:
        return 6
    elif step <= 40:
        return 7
    elif step <= 60:
        return 8
    elif step <= 80:
        return 10
    elif step <= 150:
        return 15
    elif step <= 200:
        return 20
    elif step <= 250:
        return 25
    else:
        return 30
    
def get_group_size(step):
    if step > 250:
        return 7
    elif step >150:
        return 6
    elif step >100:
        return 5    
    return 4

async def create_words_group():
    conn = await get_pg_con()
    cursor = conn.cursor()
    for lang in LANGS:
        words = []
        step = 1
        sql = f"""SELECT word, level FROM {SCHEMA}.words WHERE lang=%s order by level"""
        await cursor.execute(sql, (lang,))
        results = await cursor.fetchall()
        for r in results:
            word = r.get("word")
            level = r.get("level")
            words.append(word)
            g_size = get_group_size(step)
            if len(words) >= g_size:
                save_words = words[:g_size]
                words = words[g_size:]
                for w in save_words:
                    sql = f"""update {SCHEMA}.words set step=%s where word_id=%s and lang=%s"""
                    try:
                        await cursor.execute(sql, (step, w, lang,))
                    except Exception as e:
                        print(f"Error executing SQL: {sql}")
                        print(e)
                step += 1


async def get_word_count():
    conn = await get_pg_con()
    cursor = conn.cursor()
    for lang in LANGS:
        if lang in ["ja", "zh-Hans"]:
            continue
        sql = f"""SELECT part_id, text FROM {SCHEMA}.parts WHERE lang=%s"""
        await cursor.execute(sql, (lang,))
        results = await cursor.fetchall()
        for r in results:
            text = r.get("text")
            w_count = len(text.split())
            print(f"lang: {lang}, w_count: {w_count}, text: {text}")
            sql = f"""update {SCHEMA}.parts set wcount=%s where part_id=%s and lang=%s"""
            try:
                await cursor.execute(sql, (w_count, r.get("part_id"), lang,))
            except Exception as e:
                print(f"Error executing SQL: {sql}")
                print(e)


async def set_part_step():
    conn = await get_pg_con()
    cursor = conn.cursor()
    for l in LANGS:
        for i in range(1, 4000):
            words = []
            sql = f"""SELECT word, lang , step  FROM {SCHEMA}.words where lang=%s and step =%s"""
            await cursor.execute(sql, (l, i))
            results = await cursor.fetchall()
            if len(results) == 0:
                break
            for r in results:
                word = r.get("word")
                words.append(word)
            sql = f"""insert into {SCHEMA}.steps (lang, step_id, step, words) values (%s, %s, %s, %s)"""
            await cursor.execute(sql, (l,str(i), i, words))


async def get_word_count_no_space():
    from utils.content_gen.context import get_words_all_structure
    conn = await get_pg_con()
    cursor = conn.cursor()
    for lang in ["ja", "zh-Hans"]:
        sql = f"""SELECT part_id, text FROM {SCHEMA}.parts WHERE lang=%s"""
        await cursor.execute(sql, (lang,))
        results = await cursor.fetchall()
        for r in results:
            text = r.get("text")
            words, all_words, pos, root, propn, stop_words = get_words_all_structure(text, lang)
            print(f"lang: {lang}, w_count: {len(all_words)}, all_words: {all_words}")
            w_count = len(all_words)
            sql = f"""update {SCHEMA}.parts set wcount=%s where part_id=%s and lang=%s"""
            try:
                await cursor.execute(sql, (w_count, r.get("part_id"), lang,))
            except Exception as e:
                print(f"Error executing SQL: {sql}")
                print(e)

async def set_structure():
    from utils.content_gen.spacy_utils import get_spacy_langs
    from utils.content_gen.context import get_words_all_structure
    conn = await get_pg_con()
    cursor = conn.cursor()
    for lang in LANGS:
        if not lang in get_spacy_langs():
            continue
        sql = f"""SELECT part_id, text FROM {SCHEMA}.parts WHERE lang=%s and wcount > 1 and wcount < 12"""
        await cursor.execute(sql, (lang,))
        results = await cursor.fetchall()
        for r in results:
            text = r.get("text")
            part_id = r.get("part_id")
            # print (f"lang: {lang}, text: {text}")
            words, all_words, pos, root, propn, stop_words = get_words_all_structure(text, lang)
            # print(f"text: {text}, w_count: {pos}, root: {root}")
            sql = f"""INSERT INTO {CONTENT_SCHEMA}.prepared_sentences 
                (id, lang, words, all_words, pos, root, propn, stop_words, w_count) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            try:
                await cursor.execute(sql, (part_id, lang, words, all_words, pos, root, propn, stop_words, len(all_words),))
            except Exception as e:
                print(f"Error executing SQL: {sql}")
                print(e)


def generate_structure(lang, pos:list, length=3):
    if lang in LAST_PART_LANGS:
        return ','.join(pos[-1*length:])
    else:    
        return ','.join(pos[:length])

def generate_structure_root(pos:list, words:list, root:str):
    if not root:
        return ""
    else:
        pos_select= []
        idx = words.index(root)
        if idx == 0:
            pos_select = pos[:3]
        elif idx == len(words) -1 :
            pos_select = pos[-3:]
        else:
            pos_select = pos[idx-1:idx+2]
        det =  f",".join(pos_select)
        return det + f",{root}"


async def set_structure_prepared():
    conn = await get_pg_con()
    cursor = conn.cursor()
    sql = f"""SELECT id, lang, pos, all_words, root  FROM {CONTENT_SCHEMA}.prepared_sentences"""
    await cursor.execute(sql)
    results = await cursor.fetchall()
    for r in results:
        struct3 = generate_structure(r.get("lang"), r.get("pos"))
        struct4 = generate_structure(r.get("lang"), r.get("pos"), 4)
        strut_root = generate_structure_root(r.get("pos"), r.get("all_words"), r.get("root"))
        print(r.get("root"), struct3, struct4, strut_root)
        sql = f"""UPDATE {CONTENT_SCHEMA}.prepared_sentences SET structure3=%s, structure4=%s, structure_root=%s WHERE id=%s and lang=%s""" 
        try:
            await cursor.execute(sql, (struct3, struct4, strut_root, r.get("id"), r.get("lang")))
        except Exception as e:
            print(f"Error executing SQL: {sql}")
            print(e)        

async def collect_structure():
    conn = await get_pg_con()
    cursor = conn.cursor()

    for lang in LANGS:
        structs = {
            "s3": {},
            "s4": {},
            "s_root": {},
        }
        sql = f"""SELECT id, lang, structure3, structure4, structure_root  FROM {CONTENT_SCHEMA}.prepared_sentences where lang=%s"""
        await cursor.execute(sql, (lang,))
        results = await cursor.fetchall()
        if len(results) == 0:
            continue
        for r in results:
            structure3 = r.get("structure3")
            if structure3 not in structs["s3"]:
                structs["s3"][structure3] = set()
            structs["s3"][structure3].add(r.get("id"))
            struct4 = r.get("structure4")
            if struct4 not in structs["s4"]:
                structs["s4"][struct4] = set()
            structs["s4"][struct4].add(r.get("id"))
            struct_root = r.get("structure_root")
            if struct_root not in structs["s_root"]:
                structs["s_root"][struct_root] = set()
            structs["s_root"][struct_root].add(r.get("id"))
        sql = f"""INSERT INTO {CONTENT_SCHEMA}.structure (lang, struct_type, struct, ids, ids_count) VALUES (%s, %s, %s, %s, %s)"""
        for struct_type, struct in structs.items():
            for struct_key, ids in struct.items():
                ids_count = len(ids)
                try:
                    await cursor.execute(sql, (lang, struct_type, struct_key, list(ids), ids_count))
                except Exception as e:
                    print(f"Error executing SQL: {sql}")
                    print(e)
async def copy_structure():
    conn = await get_pg_con()
    cursor = conn.cursor()
    sql = f"""SELECT lang, struct_type, struct, ids, ids_count FROM {CONTENT_SCHEMA}.structure 
        WHERE struct_type=%s and ids_count > %s"""
    await cursor.execute(sql, ("s_root", 5))
    results = await cursor.fetchall()
    for r in results:
        lang = r.get("lang")
        struct_type = r.get("struct_type")
        struct = r.get("struct")
        root = struct.split(",")[-1]
        ids = r.get("ids")
        if len(ids) > 50:
            ids.sort(key=len)
            ids = ids[:50]
        ids_count = len(ids)
        sql = f"""SELECT step FROM {SCHEMA}.words WHERE word=%s and lang=%s"""
        await cursor.execute(sql, (root, lang))
        results = await cursor.fetchall()
        if len(results) > 0:
            step = results[0].get("step")
        else:
            step = 0
        sql = f"""INSERT INTO {SCHEMA}.structure (lang, struct_type, struct, ids, ids_count, root, step) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        try:
            await cursor.execute(sql, (lang, struct_type, struct,  ids, ids_count, root, step))
        except Exception as e:
            print(f"Error executing SQL: {sql}")
            print(e)




if __name__ == "__main__":
    import asyncio
    # asyncio.run(set_parts_rank())
    # asyncio.run(create_words_list())
    # asyncio.run(create_words_group())
    # asyncio.run(get_word_count())
    # asyncio.run(get_quiz_experiments())
    # asyncio.run(set_part_step())
    # asyncio.run(get_word_count_no_space())
    # asyncio.run(set_structure())
    # asyncio.run(set_structure_prepared())
    # asyncio.run(copy_structure())
    # asyncio.run(add_dialogues_to_step())
    # asyncio.run(add_structure_to_step1())
    asyncio.run(generate_easy_steps())
    # asyncio.run(add_lines_to_step())