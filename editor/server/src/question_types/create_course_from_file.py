from utils.db import get_query_results
import json
WORDS_SO_FAR = set()
WORDS_IN_SENTENCE = set()
HIRAGANA_SO_FAR = set()
KATAKANA_SO_FAR = set()
KANJI_SO_FAR = set()


async def augment_word_lesson(lesson: dict):
    pass 
async def augment_alphabet_lesson(lesson: dict):
    pass


async def create_course(lang, to_lang, title, description):
    sql = """
    INSERT INTO content.course(lang,to_lang,title,description) VALUES (%s, %s, %s,%s) RETURNING course_id
    """
    params = (lang, to_lang, title, description)
    res = await get_query_results(sql, params)
    return res[0].get('course_id') 

async def create_module(lang, to_lang, title, description, course_id):
    sql = """
    INSERT INTO content.module(lang,to_lang,title,description, course_id) VALUES (%s, %s, %s,%s,%s) RETURNING module_id
    """
    params = (lang, to_lang, title, description,course_id )
    res = await get_query_results(sql, params)
    return res[0].get('module_id')

async def create_lesson(lang, to_lang, title, description, course_id, module_id):
    sql = """
    INSERT INTO content.lesson(lang,to_lang,title,description, course_id, module_id) VALUES (%s, %s, %s,%s,%s,%s) RETURNING lesson_id
    """
    params = (lang, to_lang, title, description,course_id, module_id )
    res = await get_query_results(sql, params)
    return res[0].get('lesson_id')

async def create_exercise(lang, to_lang, course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type="sentence",extra_data=[]):
    
    sql = """
    INSERT INTO content.exercise(lang,to_lang,course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type,extra_data) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING exercise_id
    """
    params = (lang, to_lang,course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type,json.dumps(extra_data))
    await get_query_results(sql, params)
    
async def create_ab_exercise(lang, to_lang, course_id, module_id,lesson_id, sentence, to_sentence,options):
    sql = """
    INSERT INTO course.exercise(lang,to_lang,course_id, module_id,lesson_id, sentence, to_sentence,exercise_type, options) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING exercise_id
    """
    params = (lang, to_lang,course_id, module_id,lesson_id, sentence, to_sentence,'alphabet',options)
    await get_query_results(sql, params)



def _load_elements(folder, fname):
    res = []
    with open(f"{folder}/{fname}.csv") as f:
        for l in f.readlines():
            res.append(l.strip().split("\t"))
    return res



async def create_course_from_file(path,lang, to_lang, title, description):
    elements = _load_elements(path, "modules")
    course_id = await create_course(lang, to_lang, title, description)
    module_id = 0
    lesson_id = 0
    word = ''
    ab_type = ''
    letter = ''
    for e in elements:
        l = e
        if l[0] == "M":
            title = " ".join(l[1:]).replace("by_words","words")
            module_id = await create_module(lang, to_lang, title, title, course_id)
        elif l[0] == "L":
            if l[1] in ["greeting", "by_words"]:
                word = l[2]
                WORDS_SO_FAR.add(word)
                title = " ".join(l[1:]).replace("by_words","").strip()
                lesson_id = await create_lesson(lang, to_lang, title, title, course_id,module_id)
            elif l[1] in ["kanji","katakana",'hiragana']:
                letter = l[3]
                ab_type = l[2]
                if ab_type == "hiragana":
                    HIRAGANA_SO_FAR.add(letter)
                elif ab_type == "katakana":
                    KATAKANA_SO_FAR.add(letter)
                elif ab_type == "kanji":
                    KANJI_SO_FAR.add(letter)
        elif l[0] == "S":
            if l[1] in ["kanji","katakana",'hiragana']:
                await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, 0, 0 ,"alphabet",l)
            else:
               await create_exercise(lang, to_lang,course_id, module_id,lesson_id, l[2], l[5])




