from utils.db import get_query_results
import json

async def test_insert_get_id():
    sql = """
    INSERT INTO course.course(lang,to_lang,title,description) VALUES (%s, %s, %s,%s) RETURNING id
    """
    params = ("en","he","test","test")
    res = await get_query_results(sql, params)
    print(res)


async def create_course(lang, to_lang, title, description):
    sql = """
    INSERT INTO course.course(lang,to_lang,title,description) VALUES (%s, %s, %s,%s) RETURNING id
    """
    params = (lang, to_lang, title, description)
    res = await get_query_results(sql, params)
    return res[0].get('id')

async def create_module(lang, to_lang, title, description, course_id):
    sql = """
    INSERT INTO course.module(lang,to_lang,title,description, course_id) VALUES (%s, %s, %s,%s,%s) RETURNING id
    """
    params = (lang, to_lang, title, description,course_id )
    res = await get_query_results(sql, params)
    return res[0].get('id')

async def create_lesson(lang, to_lang, title, description, course_id, module_id):
    sql = """
    INSERT INTO course.lesson(lang,to_lang,title,description, course_id, module_id) VALUES (%s, %s, %s,%s,%s,%s) RETURNING id
    """
    params = (lang, to_lang, title, description,course_id, module_id )
    res = await get_query_results(sql, params)
    return res[0].get('id')

async def create_exercise(lang, to_lang, course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type="sentence",extra_data=[]):
    sql = """
    INSERT INTO course.exercise(lang,to_lang,course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type,extra_data) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """
    params = (lang, to_lang,course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type,json.dumps(extra_data))
    await get_query_results(sql, params)
    


def _load_elements(folder, fname):
    with open(f"{folder}/{fname}.csv") as f:
        return  f.readlines()



async def create_course_from_file(path,lang, to_lang, title, description):
    elements = _load_elements(path, "modules")
    course_id = await create_course(lang, to_lang, title, description)
    module_id = 0
    lesson_id = 0
    for e in elements:
        l = e.split("\t")
        if l[0] == "M":
            module_id = await create_module(lang, to_lang, e, e, course_id)
        elif l[0] == "L":
            lesson_id = await create_lesson(lang, to_lang, e, e, course_id,module_id)
        elif l[0] == "S":
            if l[1] in ["kanji","katakana",'hiragana']:
                await create_exercise(lang, to_lang,course_id, module_id,lesson_id, 0, 0 ,"alphabet",l)
            else:
               await create_exercise(lang, to_lang,course_id, module_id,lesson_id, l[2], l[5])






