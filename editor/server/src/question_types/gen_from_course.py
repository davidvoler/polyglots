from utils.db import get_query_results, run_query
from question_types.memory_game import create_memory_game
from question_types.exercise_model import ExerciseModel

import random
import json


WORDS_SO_FAR = set()
WORDS_IN_SENTENCE = set()
HIRAGANA_SO_FAR = []
KATAKANA_SO_FAR = []
KANJI_SO_FAR = []
MIN_CHANGE_DIRECTION = 30

REPEAT_AFTER_KANA = 10
REPEAT_AFTER_KANJI = 20

HIRAGANA_REPEAT = []
KATAKANA_REPEAT = []
KANJI_REPEAT = []


async def augment_alphabet_lesson_mem_game(exercise:ExerciseModel,ab_type: str, ab_letter: str,letter_collection:list):
    letters = letter_collection.copy()
    try:
        letters.remove(ab_letter)
    except:
        pass
    grid = create_memory_game(letters[:7]+[ab_letter], 4, 4)
    exercise.extra_data['memory_game'] = grid
    exercise.type = "memory_game"
    exercise.title = f"Memory Game - {ab_letter}"
    exercise.word = ''
    exercise.letter = ab_letter
    exercise.ab_type = ab_type
    exercise.correct_options = []
    exercise.wrong_options = []
    exercise.annotated_sentence = {}
    await save_exercise_new_format(exercise)



async def augment_alphabet_lesson_letter_in_words(exercise:ExerciseModel,ab_type: str, ab_letter: str,words_collection:list):
    words_with_letter = []
    words_without_letter = []
    for word in words_collection:
        if ab_letter in word:
            words_with_letter.append(word)
        else:
            words_without_letter.append(word)
    exercise.type = "letters_in_words"
    exercise.word = ''
    exercise.correct_options = words_with_letter
    exercise.wrong_options = words_without_letter[:6]
    exercise.letter = ab_letter
    await save_exercise_new_format(exercise)




async def save_exercise_new_format(exercise: ExerciseModel):
    sql = """
    INSERT INTO content.exercise(lesson_id, module_id, course_id, exercise_type, lang, to_lang, title, instruction, sentence, extra_data, annotated_sentence, word, letter, verb, 
    verb_lemma, noun, adjective, auxiliary, ab_type, sentence_id, to_sentence_id, correct_options, wrong_options, audio_link)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    await run_query(sql, (exercise.lesson_id, exercise.module_id, exercise.course_id, exercise.exercise_type, exercise.lang, exercise.to_lang, exercise.title, exercise.instruction, exercise.sentence,
    json.dumps(exercise.extra_data), json.dumps(exercise.annotated_sentence), exercise.word, exercise.letter, exercise.verb, exercise.verb_lemma, exercise.noun, exercise.adjective, exercise.auxiliary, 
    exercise.ab_type, exercise.sentence_id, exercise.to_sentence_id, exercise.correct_options, exercise.wrong_options, exercise.audio_link))

async def augment_exercise(old_exercise: dict, new_exercise: ExerciseModel):
    words_count = len(WORDS_SO_FAR)
    print(words_count)
   

async def augment_lesson(lesson: dict,new_course_id: int, new_module_id: int, new_lesson_id: int):
    title = lesson.get('title')
    lesson_type = ""
    lesson_word = ""
    ab_type = ""
    exercise = ExerciseModel(
        lesson_id=new_lesson_id,
        module_id=new_module_id,
        course_id=new_course_id,
        lang=lesson.get('lang'),
        to_lang=lesson.get('to_lang'),
    )
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
            HIRAGANA_SO_FAR.append(lesson_word)
            await augment_alphabet_lesson_mem_game(exercise, ab_type, lesson_word, list(HIRAGANA_SO_FAR))
            await augment_alphabet_lesson_letter_in_words(exercise, ab_type, lesson_word, list(WORDS_SO_FAR))
            HIRAGANA_REPEAT.append(lesson_word)
            if len(HIRAGANA_REPEAT) >= REPEAT_AFTER_KANA:
                ab_letter = HIRAGANA_REPEAT[0]
                HIRAGANA_REPEAT = HIRAGANA_REPEAT[1:]
                await augment_alphabet_lesson_mem_game(exercise, ab_type, ab_letter, HIRAGANA_SO_FAR)
                await augment_alphabet_lesson_letter_in_words(exercise, ab_type, ab_letter, list(WORDS_SO_FAR))
        elif ab_type == "katakana":
            KATAKANA_SO_FAR.append(lesson_word)
            await augment_alphabet_lesson_mem_game(exercise, ab_type, lesson_word, KATAKANA_SO_FAR)
            await augment_alphabet_lesson_letter_in_words(exercise, ab_type, lesson_word, list(WORDS_SO_FAR))
            KATAKANA_REPEAT.append(lesson_word)
            if len(KATAKANA_REPEAT) >= REPEAT_AFTER_KANA:
                ab_letter = KATAKANA_REPEAT[0]
                KATAKANA_REPEAT = KATAKANA_REPEAT[1:]
                await augment_alphabet_lesson_mem_game(exercise, ab_type, ab_letter, KATAKANA_SO_FAR)
                await augment_alphabet_lesson_letter_in_words(exercise, ab_type, ab_letter, list(WORDS_SO_FAR))
        elif ab_type == "kanji":
            KANJI_SO_FAR.append(lesson_word)
            await augment_alphabet_lesson_mem_game(exercise, ab_type, lesson_word, KANJI_SO_FAR)
            await augment_alphabet_lesson_letter_in_words(exercise, ab_type, lesson_word, list(WORDS_SO_FAR))
            KANJI_REPEAT.append(lesson_word)
            if len(KANJI_REPEAT) >= REPEAT_AFTER_KANJI:
                ab_letter = KANJI_REPEAT[0]
                KANJI_REPEAT = KANJI_REPEAT[1:]
                await augment_alphabet_lesson_mem_game(exercise, ab_type, ab_letter, KANJI_SO_FAR)
                await augment_alphabet_lesson_letter_in_words(exercise, ab_type, ab_letter, list(WORDS_SO_FAR))        
    
    else:
        lesson_type = "words"
        lesson_word = title
        WORDS_SO_FAR.add(lesson_word)
    sql = """
    select * from course.exercise where lesson_id = %s
    """
    old_lesson_id = lesson.get('id')
    results = await get_query_results(sql, (old_lesson_id,))
    exercise = ExerciseModel(
        lesson_id=new_lesson_id,
        module_id=new_module_id,
        course_id=new_course_id,
        lang=lesson.get('lang'),
        to_lang=lesson.get('to_lang'),
    )
    for r in results:
        if lesson_type == "alphabet":
            exercise.exercise_type = 'letter_in_words_single_choice'
            exercise.letter = lesson_word
            exercise.ab_type = ab_type
        else:
            exercise.exercise_type = 'sentence_single_choice'
            exercise.word = lesson_word
            exercise.sentence_id = r.get('sentence_id')
            exercise.to_sentence_id = r.get('to_sentence_id')
            exercise.annotated_sentence = r.get('annotated_sentence')
        exercise.correct_options = [r.get('to_sentence')]
        exercise.wrong_options = r.get('to_options')
        exercise.audio_link = r.get('audio_link')
        await save_exercise_new_format(exercise)
        if lesson_type == "words":
            await augment_exercise(r, exercise)

async def gen_from_lesson(lesson: dict,new_course_id: int, new_module_id: int):
    old_module_id = lesson.get('id')
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
    old_course_id = module.get('id')
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

async def gen_from_course(folder_name: str, file_name: str):
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
    insert into content.course (lang,to_lang,title,description) values (%s,%s,%s,%s) returning course_id
    """
    print(sql)
    print(lang, to_lang, title, description)
    results = await get_query_results(sql, (lang, to_lang, title, description))
    new_course_id = results[0].get('course_id')
    await gen_from_module(course, new_course_id)