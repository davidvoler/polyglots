from editor.server.src.generators.course_from_file_question_types import WORDS_IN_SENTENCE
from utils.db import get_query_results, run_query
from question_types.identify_words_in_speech import identify_words_in_speech
from question_types.letter_in_words import letter_in_words
from question_types.memory_game import create_memory_game
from question_types.sentences_multiple_choice import sentences_multiple_choice
from question_types.sentences_single_choice import sentences_single_choice
from question_types.type_text import type_text
from question_types.words_in_grid import words_in_grid
import random

WORDS_SO_FAR = set()
WORDS_IN_SENTENCE = set()
HIRAGANA_SO_FAR = set()
KATAKANA_SO_FAR = set()
KANJI_SO_FAR = set()
MIN_CHANGE_DIRECTION = 30






async def augment_alphabet_exercise(exercise: dict, new_course_id: int, new_module_id: int, new_lesson_id: int, ab_type: str, ab_letter: str):
    if ab_type == "hiragana":
        if len(HIRAGANA_SO_FAR) > 6:
            letters = list(HIRAGANA_SO_FAR)
            random.shuffle(letters)
            try:
                letters.remove(ab_letter)
            except:
                pass
            memory_game = create_memory_game(letters[:6]+[ab_letter], 4, 4)
    elif ab_type == "katakana":
        KATAKANA_SO_FAR.add(lesson_word)
    elif ab_type == "kanji":
        KANJI_SO_FAR.add(lesson_word)
async def augment_greeting_exercise(exercise: dict, new_course_id: int, new_module_id: int, new_lesson_id: int, lesson_word: str):
    pass 


async def augment_words_exercise(exercise: dict, new_course_id: int, new_module_id: int, new_lesson_id: int, lesson_word: str):
    words_count = len(WORDS_SO_FAR)
    if words_count > 10:
        pass 
    if words_count > 50:
        pass 
    if words_count > 100:
        pass 

async def save_exercise_new_format(exercise: dict, new_course_id: int, new_module_id: int, new_lesson_id: int, lesson_type: str, lesson_word: str):
    pass


async def augment_exercise(exercise: dict, new_course_id: int, new_module_id: int, new_lesson_id: int, lesson_type: str, lesson_word: str, ab_type: str):
    if lesson_type == "alphabet":
        await augment_alphabet_exercise(exercise, new_course_id, new_module_id, new_lesson_id, ab_type)
    elif lesson_type == "greeting": 
        await augment_greeting_exercise(exercise, new_course_id, new_module_id, new_lesson_id, lesson_word)
    elif lesson_type == "words":
        await augment_words_exercise(exercise, new_course_id, new_module_id, new_lesson_id, lesson_word)
    await save_exercise_new_format(exercise, new_course_id, new_module_id, new_lesson_id, lesson_type, lesson_word)


async def augment_lesson(lesson: dict,new_course_id: int, new_module_id: int, new_lesson_id: int):
    title = lesson.get('title')
    lesson_type = ""
    lesson_word = ""
    ab_type = ""
    if "greeting" in title.lower():
        l = title.split(" ")
        lesson_type = "greeting"
        lesson_word = l[1]
    elif "alphabet" in title.lower():
        l = title.split(" ")
        lesson_type = "alphabet"
        lesson_word = l[2]
        ab_type = l[1]
        if ab_type == "hiragana":
            HIRAGANA_SO_FAR.add(lesson_word)
        elif ab_type == "katakana":
            KATAKANA_SO_FAR.add(lesson_word)
        elif ab_type == "kanji":
            KANJI_SO_FAR.add(lesson_word)
    else:
        lesson_type = "words"
        lesson_word = title
    
    sql = """
    select * from course.exercise where lesson_id = %s
    """
    old_lesson_id = lesson.get('id')
    results = await get_query_results(sql, (old_lesson_id,))
    for r in results:
        await augment_exercise(r,new_course_id, new_module_id, new_lesson_id, lesson_type, lesson_word,ab_type)


async def gen_from_lesson(lesson: dict,new_course_id: int, new_module_id: int):
    old_module_id = lesson.get('module_id')
    old_course_id = lesson.get('course_id')
    sql = """
    SELECT * FROM course.lesson WHERE course_id = %s and module_id = %s
    """
    insert_sql = """
    INSERT INTO content.lesson(lang,to_lang,title,description, course_id, module_id) VALUES (%s,%s,%s,%s,%s,%s)
    returning lesson_id
    """
    results = await get_query_results(sql, (old_course_id, old_module_id))
    for r in results:
        lang = r.get('lang')
        to_lang = r.get('to_lang')
        title = r.get('title')
        description = r.get('description')
        res = await get_query_results(insert_sql, (lang, to_lang, title, description, new_course_id, new_module_id))
        new_lesson_id = res[0].get('lesson_id')
        await augment_lesson(r, new_course_id, new_module_id, new_lesson_id)
  
async def gen_from_module(module: dict, new_course_id: int):
    old_course_id = module.get('course_id')
    sql = """
    SELECT * FROM course.module WHERE course_id = %s
    """
    insert_sql = """
    INSERT INTO content.module(lang,to_lang,title,description, course_id) VALUES (%s,%s,%s,%s,%s)
    returning module_id
    """
    results = await get_query_results(sql, (old_course_id,))
    for r in results:
        lang = r.get('lang')
        to_lang = r.get('to_lang')
        title = r.get('title')
        description = r.get('description')
        res = await get_query_results(insert_sql, (lang, to_lang, title, description, new_course_id))
        new_module_id = res[0].get('module_id')
        await gen_from_lesson(r, new_course_id, new_module_id)

async def gen_from_course(course_id: int):
    sql = """
    SELECT * FROM course.course WHERE id = %s
    """
    results = await get_query_results(sql, (course_id,))
    course = results[0]
    lang = course.get('lang')
    to_lang = course.get('to_lang')
    title = course.get('title')
    description = course.get('description')
    
    sql = """
    SELECT insert into content.course(lang,to_lang,title,description) values (%s,%s,%s,%s)
    returning course_id
    """
    results = await get_query_results(sql, (lang, to_lang, title, description))
    new_course_id = results[0].get('course_id')
    await gen_from_module(course, new_course_id)