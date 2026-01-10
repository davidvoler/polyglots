from utils.db import get_query_results
from question_types.exercise_model import ExerciseModel
import json
from question_types.identify_words_in_speech import create_identify_words_in_speech_exercise
from question_types.letter_in_words import create_letter_in_words_exercise
from question_types.memory_game import create_memory_game_exercise
from question_types.sentences_multiple_choice import create_multiple_choice_sentence_exercise
from question_types.sentences_single_choice import create_single_choice_sentence_exercise
from question_types.type_question import create_type_question_exercise
from question_types.words_in_grid import create_words_in_grid_exercise


WORDS_SO_FAR = set()
WORDS_IN_SENTENCE = set()
HIRAGANA_SO_FAR = set()
KATAKANA_SO_FAR = set()
KANJI_SO_FAR = set()

REPEAT_AFTER_KANA = 10
REPEAT_AFTER_KANJI = 15

HIRAGANA_REPEAT = []
KATAKANA_REPEAT = []
KANJI_REPEAT = []


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

async def load_sentences(sentence_id, lang):
    sql = """
    SELECT sentence, to_sentence FROM content_raw.sentence_elements WHERE id = %s and lang = %s
    """
    params = (sentence_id, lang)
    res = await get_query_results(sql, params)
    return res[0]

async def create_sentence_exercise(lang, to_lang, course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type="sentence",extra_data=[]):
    sentence = await load_sentences(sentence_id, lang)
    to_sentence = await load_sentences(to_sentence_id, to_lang)
    exercise = ExerciseModel(
        lang=lang,
        to_lang=to_lang,
        course_id=course_id,
        module_id=module_id,
        lesson_id=lesson_id,
        sentence_id=sentence_id,
        to_sentence_id=to_sentence_id,
    )
    await create_single_choice_sentence_exercise(exercise, sentence, to_sentence)
    await create_multiple_choice_sentence_exercise(exercise, sentence, to_sentence)
    await question_type_identify_words_in_speech(exercise, sentence, to_sentence)
    

async def create_lesson_word_exercise(lang, to_lang, course_id, module_id,lesson_id, word):
    learned_chars = 0
    for c in word:
        if c in HIRAGANA_SO_FAR:
            learned_chars += 1
        elif c in KATAKANA_SO_FAR:
            learned_chars += 1
        elif c in KANJI_SO_FAR:
            learned_chars += 1
    if learned_chars/len(word) < 0.7:
        return
    exercise = ExerciseModel(
        lang=lang,
        to_lang=to_lang,
        course_id=course_id,
        module_id=module_id,
        lesson_id=lesson_id,
        word=word,
    )
    await create_type_question_exercise(exercise, word)


async def create_ab_exercise(lang, to_lang, course_id, module_id,lesson_id, letter, ab_type, word_collection):
    exercise = ExerciseModel(
        lang=lang,
        to_lang=to_lang,
        course_id=course_id,
        module_id=module_id,
        lesson_id=lesson_id,
        letter=letter,
        ab_type=ab_type,
    )
    await create_letter_in_words_exercise(exercise, letter, word_collection, list(WORDS_SO_FAR))



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
                await create_lesson_word_exercise(lang, to_lang,course_id, module_id,lesson_id, word)
            elif l[1] in ["kanji","katakana",'hiragana']:
                letter = l[3]
                ab_type = l[2]
                if ab_type == "hiragana":
                    HIRAGANA_SO_FAR.add(letter)
                    HIRAGANA_REPEAT.append(letter)
                    if len(HIRAGANA_REPEAT) >= REPEAT_AFTER_KANA:
                        letter = HIRAGANA_REPEAT[0]
                        HIRAGANA_REPEAT = HIRAGANA_REPEAT[1:]
                        await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, letter, ab_type, list(HIRAGANA_SO_FAR))
                elif ab_type == "katakana":
                    KATAKANA_SO_FAR.add(letter)
                    KATAKANA_REPEAT.append(letter)
                    if len(KATAKANA_REPEAT) >= REPEAT_AFTER_KANA:
                        letter = KATAKANA_REPEAT[0]
                        KATAKANA_REPEAT = KATAKANA_REPEAT[1:]
                        await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, letter, ab_type, list(KATAKANA_SO_FAR))
                elif ab_type == "kanji":
                    KANJI_SO_FAR.add(letter)
                    KANJI_REPEAT.append(letter)
                    if len(KANJI_REPEAT) >= REPEAT_AFTER_KANJI:
                        letter = KANJI_REPEAT[0]
                        KANJI_REPEAT = KANJI_REPEAT[1:]
                        await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, letter, ab_type, list(KANJI_SO_FAR))
        elif l[0] == "S":
            if l[1] in ["kanji","katakana",'hiragana']:
                await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, l[1], l[2], l[3:])
            else:
               await create_exercise(lang, to_lang,course_id, module_id,lesson_id, l[2], l[5])




