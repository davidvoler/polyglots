import pymongo
from pydantic import BaseModel
from utils.db import get_pg_con
import random

client = pymongo.MongoClient()
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

LANGS_NO_SPACY = [
'ar',
'cs',
'hi',
'he',   
]

class Field(BaseModel):
    mongo_name: str
    pg_name: str
    default: str = None
    lower: bool = False

def escape_string(value):
    return value.replace("'", "''")

async def insert_row(document:dict, schema:str, table:str, fields:list[Field], conn):
    values = []
    insert_fields = []
    for field in fields:
        if field.default:
            values.append(field.default)
        elif field.lower:
            values.append(document[field.mongo_name].lower())
        else:
            values.append(document[field.mongo_name])
        insert_fields.append(field.pg_name)
    values_str = ','.join([f"'{escape_string(value)}'" if isinstance(value, str) else str(value) for value in values])
    sql = f"""
    INSERT INTO {schema}.{table} ({','.join(insert_fields)} )
    VALUES ({values_str});
    """
    print(sql)
    try:
        await conn.execute(sql)
        await conn.commit()
    except Exception as e:
        await conn.rollback()
        print(f"Error executing SQL: {sql}")
        print(e)

    
    
async def export_collection(db_name, collection_name, schema, table, fields):
    conn = await get_pg_con()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        await insert_row(document, schema, table, fields,  conn)        



async def insert_row_inline( _id, lang,document:dict, schema:str, table:str, fields:list[Field], conn):
    values = [_id, lang]
    insert_fields = ['part_id', 'lang']
    for field in fields:
        val = ""
        if field.default:
            val = field.default
        elif field.lower:
            val = document[field.mongo_name].lower()
        else:
            val = document.get(field.mongo_name)
        if type(val) == list:
            escaped = [escape_string(v) for v in val]
        elif type(val) == str:
            escaped = escape_string(val)
        else:
            escaped = val   
        if not escaped:
            continue
        values.append(escaped)
        insert_fields.append(field.pg_name)
    values_type = []
    for v in values:
        if type(v) == list:
            v = [escape_string(i) for i in v]
            values_type.append(f"ARRAY{str(v)}")
        elif type(v) == str:
            v = escape_string(v)
            values_type.append(f"'{v}'")
        else:
            values_type.append(str(v))

    values_str = ','.join(values_type)
    sql = f"""
    INSERT INTO {schema}.{table} ({','.join(insert_fields)} )
    VALUES ({values_str});
    """
    print(sql)
    try:
        await conn.execute(sql)
        await conn.commit()
    except Exception as e:
        await conn.rollback()
        print(f"Error executing SQL: {sql}")
        print(e)

async def export_collection_inline(db_name, collection_name, schema, table, fields):
    conn = await get_pg_con()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        _id = document.get("_id")
        _id = escape_string(_id)
        if not _id:
            continue
        for key, val in document.items():
            if type(val) == dict:
                await insert_row_inline(_id, key, val, schema, table, fields,  conn)        



async def export_collection_inline_params(db_name, collection_name, schema, table, fields):
    conn = await get_pg_con()
    pg_cursor = conn.cursor()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        _id = document.get("_id")
        if not _id:
            continue
        for key, val in document.items():
            if type(val) == dict:
                try:
                    await pg_cursor.execute( f"""
                        INSERT INTO {schema}.{table} (part_id, lang, text, recording, options, words)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """, (_id, key, val.get("text"), val.get("rec"), val.get("options"), val.get("ranked")))
                    await pg_cursor.connection.commit()
                except Exception as e:
                    await pg_cursor.connection.rollback()
                    print(f"Error executing SQL: ")
                    print(e)

async def export_collection_dialogue(db_name, collection_name):
    conn = await get_pg_con()
    pg_cursor = conn.cursor()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        _id = document.get("_id")
        tag = document.get("tag").lower().strip()
        subject = document.get("subject").lower().strip()
        if not _id:
            continue
        for key, val in document.items():
            if type(val) == dict:
                try:
                    await pg_cursor.execute( f"""
                        INSERT INTO polyglots_quiz.dialogue (lang, dialogue_id, tag)
                        VALUES (%s, %s, %s);
                        """, (key,_id, tag))
                    await pg_cursor.connection.commit()
                except Exception as e:
                    await pg_cursor.connection.rollback()
                    print(f"Error executing SQL: ")
                    print(e)

async def export_collection_dialogue_lines(db_name, collection_name):
    conn = await get_pg_con()
    pg_cursor = conn.cursor()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        _id = document.get("_id")
        dialogue_id = document.get("dialogue_id")
        line_no = document.get("line_no")
        if not _id:
            continue
        for key, val in document.items():
            if type(val) == dict:
                try:
                    await pg_cursor.execute( f"""
                        INSERT INTO polyglots_quiz.dialogue_line (lang, dialogue_id, dialogue_line,line_no, text, words, recording, options)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """, (key, dialogue_id, _id, line_no,val.get("text"), val.get("ranked"), val.get("rec"), val.get("options")))
                    await pg_cursor.connection.commit()
                except Exception as e:
                    await pg_cursor.connection.rollback()
                    print(f"Error executing SQL: ")
                    print(e)


async def export_collection_tags(db_name, collection_name):
    conn = await get_pg_con()
    pg_cursor = conn.cursor()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        _id = document.get("_id").strip().lower()
        tag = document.get("_id").strip()
        dialogues = document.get("dialogues")
        parts = document.get("parts")
        if not _id:
            continue
        for l in LANGS:
            try:
                await pg_cursor.execute( f"""
                    INSERT INTO polyglots_quiz.tags (lang, tag_id, tag, dialogues, parts)
                    VALUES (%s, %s, %s, %s, %s);
                    """, (l, _id, tag,dialogues, parts))
                await pg_cursor.connection.commit()
            except Exception as e:
                await pg_cursor.connection.rollback()
                print(f"Error executing SQL: ")
                print(e)


async def export_steps(db_name, collection_name):
    conn = await get_pg_con()
    pg_cursor = conn.cursor()
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        _id = document.get("_id").strip().lower()
        tag = document.get("_id").strip()
        dialogues = document.get("dialogues")
        parts = document.get("parts")
        if not _id:
            continue
        for l in LANGS:
            try:
                await pg_cursor.execute( f"""
                    INSERT INTO polyglots_quiz.tags (lang, tag_id, tag, dialogues, parts)
                    VALUES (%s, %s, %s, %s, %s);
                    """, (l, _id, tag,dialogues, parts))
                await pg_cursor.connection.commit()
            except Exception as e:
                await pg_cursor.connection.rollback()
                print(f"Error executing SQL: ")
                print(e)




async def add_words_to_dialogues():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    client = pymongo.MongoClient()
    dialogues = client.quiz.dialogues.find()
    for d in dialogues:
        l_words = {}
        dialogue_id = d.get("_id")
        if not dialogue_id:
            continue
        lines = client.quiz.dialogue_lines.find({"dialogue_id": dialogue_id})
        for line in lines:
            for key, val in line.items():
                if type(val) == dict:
                    words= val.get("ranked", [])
                    if key not in l_words:
                        l_words[key] = set()
                    for w in words:
                        l_words[key].add(w)
        print(l_words)
        for key, val in l_words.items():
            sql = f"""
            UPDATE polyglots_quiz.dialogue
            SET words = %s
            WHERE lang =%s AND dialogue_id =%s;
            """
            await pg_cursor.execute(sql, (list(val), key, dialogue_id))


async def step_add_words():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    
    for l in LANGS:
        for i in range(1, 1000):
            words = []
            sql = f"""
            SELECT step, word FROM polyglots_quiz.words WHERE lang=%s and step=%s;
            """
            await pg_cursor.execute(sql, (l, i))
            res = await pg_cursor.fetchall()
            if not res:
                continue
            for r in res:
                words.append(r.get("word"))
            print(i, words)
            
            sql = f"""
                INSERT INTO polyglots_quiz.steps (lang, step_id, step, words)
                VALUES (%s, %s, %s, %s);
                """
            await pg_cursor.execute(sql, (l, str(i), i, words,))        


async def add_dialogues_to_step():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        for i in range(1, 1600):
            dialogues_ids = []
            sql = f"""
            SELECT lang, step_id, words  FROM polyglots_quiz.steps1 WHERE lang=%s and step_id=%s; 
            """
            await pg_cursor.execute(sql, (l, str(i)))
            res = await pg_cursor.fetchall()
            words = []
            if not res:
                continue
            for r in res:
                words = r.get("words")
            if not words:
                continue
            print(l, i, words)
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT dialogue_id, words FROM polyglots_quiz.dialogue WHERE lang=%s and words && ARRAY[{placeholder}]::varchar[];
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            res = await pg_cursor.fetchall()
            for r in res:
                d_words = r.get("words")
                dialogue_id = r.get("dialogue_id")
                if len(set(d_words) & set(words)) > 1:
                    dialogues_ids.append(dialogue_id)
            print(dialogues_ids)
            sql = f"""
                UPDATE polyglots_quiz.steps
                SET dialogues = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (dialogues_ids, l, str(i)))

async def add_structure_to_step():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        for i in range(1, 1600):
            ids = []
            sql = f"""
            SELECT lang, step_id, words  FROM polyglots_quiz.steps1 WHERE lang=%s and step_id=%s; 
            """
            await pg_cursor.execute(sql, (l, str(i)))
            res = await pg_cursor.fetchall()
            words = []
            if not res:
                continue
            for r in res:
                words = r.get("words")
            if not words:
                continue
            print(l, i, words)
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT ids FROM polyglots_quiz.structure WHERE lang=%s and root in ({placeholder});
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            res = await pg_cursor.fetchall()
            for r in res:
                ids = ids + r.get("ids", [])
            print(ids)
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET structure = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (ids, l, str(i)))


async def add_parts_to_step():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        for i in range(1, 1600):
            ids = []
            sql = f"""
            SELECT lang, step_id, words  FROM polyglots_quiz.steps1 WHERE lang=%s and step_id=%s; 
            """
            await pg_cursor.execute(sql, (l, str(i)))
            res = await pg_cursor.fetchall()
            words = []
            if not res:
                continue
            for r in res:
                words = r.get("words")
            if not words:
                continue
            print(l, i, words)
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT part_id FROM polyglots_quiz.parts WHERE lang=%s and words && ARRAY[{placeholder}]::varchar[];
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            res = await pg_cursor.fetchall()
            for r in res:
                ids.append(r.get("part_id"))
            
            
            ids.sort(key=len)
            #max 60
            sample = random.sample(ids, min(30, len(ids)))
            ids = ids[:30+int(i/2)] + sample
            ids = list(set(ids))
            ids.sort(key=len)
            print(ids, len(ids))
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET parts = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (ids, l, str(i)))


async def add_lines_to_step():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        for i in range(1, 1600):
            lines = []
            sql = f"""
            SELECT lang, step_id, words  FROM polyglots_quiz.steps WHERE lang=%s and step_id=%s; 
            """
            await pg_cursor.execute(sql, (l, str(i)))
            res = await pg_cursor.fetchall()
            words = []
            if not res:
                continue
            for r in res:
                words = r.get("words")
            if not words:
                continue
            print(l, i, words)
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT dialogue_id, dialogue_line FROM polyglots_quiz.dialogue_line WHERE lang=%s and words && ARRAY[{placeholder}]::varchar[];
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            res = await pg_cursor.fetchall()
            for r in res:
                dialogue_id = r.get("dialogue_id")
                dialogue_line = r.get("dialogue_line") 
                lines.append(f"{dialogue_id}_{dialogue_line}")
            lines.sort(key=len)
            lines = list(set(lines))
            random.shuffle(lines)
            lines = lines[:20]
            print(lines)
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET lines = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (lines, l, str(i)))
    

async def add_more_dialogues():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        pass


async def add_structure_to_step1():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        steps = []
        sql = f"""
        SELECT lang, step_id, words  FROM polyglots_quiz.steps1 WHERE lang=%s; 
        """
        await pg_cursor.execute(sql, (l, ))
        res = await pg_cursor.fetchall()
        for r in res:
            words = r.get("words")
            if not words:
                continue
            print(l, words)
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT ids FROM polyglots_quiz.structure WHERE lang=%s and root in ({placeholder});
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            print(params)
            print(sql)
            res1 = await pg_cursor.fetchall()
            ids = []
            for r1 in res1:
                ids = ids + r1.get("ids", [])
            print(ids)
            if not ids:
                continue
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET structure = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (ids, l, r.get("step_id")))



async def add_parts_to_step1():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
        sql = f"""
        SELECT lang, step_id, words  FROM polyglots_quiz.steps1 WHERE lang=%s; 
        """
        await pg_cursor.execute(sql, (l, ))
        res = await pg_cursor.fetchall()
        for r in res:
            i = int(r.get("step_id"))
            words = r.get("words")
            if not words:
                continue
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT part_id FROM polyglots_quiz.parts WHERE lang=%s and words && ARRAY[{placeholder}]::varchar[];
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            res1 = await pg_cursor.fetchall()
            ids = []
            for r1 in res1:
                ids.append(r1.get("part_id"))
            ids.sort(key=len)
            #max 60
            sample = random.sample(ids, min(30, len(ids)))
            ids = ids[:30+int(i/2)] + sample
            ids = list(set(ids))
            ids.sort(key=len)
            print(ids, len(ids))
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET parts = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (ids, l, str(i)))

async def add_lines_to_step1():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS:
       
        
        sql = f"""
        SELECT lang, step_id, words  FROM polyglots_quiz.steps1 WHERE lang=%s; 
        """
        await pg_cursor.execute(sql, (l,))
        steps = await pg_cursor.fetchall()
        for s in steps:
            words = s.get("words")
            if not words:
                continue
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT dialogue_id, dialogue_line FROM polyglots_quiz.dialogue_line WHERE lang=%s and words && ARRAY[{placeholder}]::varchar[];
            """
            params = [l] + words
            await pg_cursor.execute(sql, tuple(params))
            res = await pg_cursor.fetchall()
            lines = []
            dialogue_ids = []
            for r in res:
                dialogue_id = r.get("dialogue_id")
                dialogue_line = r.get("dialogue_line") 
                lines.append(dialogue_line)
                dialogue_ids.append(dialogue_id)
            lines = list(set(lines))
            dialogue_ids = list(set(dialogue_ids))
            random.shuffle(lines)
            random.shuffle(dialogue_ids)
            lines = lines[:20]
            dialogue_ids = dialogue_ids[:5]
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET 
                    lines = %s,
                    dialogues = %s
                WHERE lang =%s AND step_id =%s;
                """
            await pg_cursor.execute(sql, (lines,dialogue_ids, l, s.get('step_id')))
    



async def add_structure_to_missing_spacy():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    for l in LANGS_NO_SPACY:
        sql = f"""
        SELECT lang, step_id, words, parts  FROM polyglots_quiz.steps1 WHERE lang=%s; 
        """
        await pg_cursor.execute(sql, (l, ))
        steps = await pg_cursor.fetchall()
        for s in steps:
            step_id = s.get("step_id")
            words = s.get("parts", [])[:8]
            if not words:
                continue
            print(l, step_id, words)
            placeholder = ','.join(['%s'] * len(words))
            sql = f"""
            SELECT ids FROM polyglots_quiz.structure WHERE lang=%s and root in ({placeholder});
            """
            await pg_cursor.execute(sql, tuple(['en']+ words))
            res = await pg_cursor.fetchall()
            ids = []
            for r in res:
                ids = ids + r.get("ids", [])
            print(ids)
            if not ids:
                continue
            sql = f"""
                UPDATE polyglots_quiz.steps1
                SET structure = %s
                WHERE lang =%s AND step_id =%s
                
                """
            await pg_cursor.execute(sql, (ids, l, step_id))






def get_step_word_count(step:int):
    if step < 30:
        return 1, 5
    elif step < 60:
        return 2, 6
    elif step  < 100:
        return 3, 10
    return 4, 25

def get_step_wcount(step:int):
    if step< 400:
        return int(round(step/100)) +1
    if step< 500:
        return int(round(step/100)) +3
    if step< 600:
        return int(round(step/100)) +4
    return 15


async def generate_easy_steps():
    con = await get_pg_con()
    pg_cursor = con.cursor()
    
    for lang in LANGS:
        i = 0
        sql = f"""
        SELECT *  
        FROM polyglots_quiz.words 
        WHERE lang=%s
        ORDER BY level;
        """
        await pg_cursor.execute(sql, (lang,))
        steps = await pg_cursor.fetchall()
        for s in steps:
            i+=1
            word = s.get("word")
            level = s.get("level", 0)
            w_count = get_step_wcount(level)
            print(f"Processing word: {word}, level: {level} w_count: {w_count}")
            sql = f"""
                SELECT * FROM polyglots_quiz.parts 
                WHERE lang=%s and words && ARRAY[%s]::varchar[];
            """
            await pg_cursor.execute(sql, (lang, word))
            parts = await pg_cursor.fetchall()
            p_w_limit = []
            p_all = []
            for p in parts:
                part_id = p.get("part_id")
                p_w_count = p.get("wcount", 0)
                if p_w_count <= w_count:
                    p_w_limit.append(part_id)
                else:
                    p_all.append(part_id)
            p_all.sort(key=len)
            p_w_limit.sort(key=len)
            sql = f"""
                SELECT * FROM polyglots_quiz.dialogue_line 
                WHERE lang=%s and words && ARRAY[%s]::varchar[];
            """
            await pg_cursor.execute(sql, (lang, word))
            lines= await pg_cursor.fetchall()
            line_to_add = []
            for l in  lines:
                txt = l.get("text", "") 
                line_id = l.get("dialogue_line")
                if lang in ['zh-Hans', 'ja']:
                    l_w_count = (int(round(len(txt)/3)))
                else:
                    l_w_count = len(txt.split())
                if l_w_count <= w_count:
                    line_to_add.append(l.get("dialogue_line"))
            sql = f"""
                SELECT * FROM polyglots_quiz.structure 
                WHERE lang=%s and root=%s
            """
            print(word, type(word))
            await pg_cursor.execute(sql, (lang, word))
            structs = await pg_cursor.fetchall()
            structs_to_add = []
            for l in structs:
                struct_ids = l.get("ids")
                structs_to_add += struct_ids
                
            sql = f"""
                INSERT INTO polyglots_quiz.step_words(lang, word, step, level, parts, all_parts, pcount, pall_count, lines, structure) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            await pg_cursor.execute(sql, (lang, word, i, level, p_w_limit, p_all, len(p_w_limit), len(p_all), line_to_add, structs_to_add))
            await pg_cursor.connection.commit()