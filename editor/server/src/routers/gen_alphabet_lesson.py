from fastapi import APIRouter
from pydantic import BaseModel
from utils.db import get_query_results
import random
router = APIRouter()    

class Options(BaseModel):
    option: str
    is_correct: bool

class Exercise(BaseModel):
    exercise_type: str
    sentence: str = ''
    options: list[Options]
    type_text: str = ''
    letters: list[str] = []

class GenLessonRequest(BaseModel):
    word: str
    lang: str
    to_lang: str
    sentence_id: int = 0
    to_sentence_id: int = 0
    words_so_far: list[str]
    words_so_far_in_sentences: list[str]
    letters_so_far: list[any]
    is_alphabet: bool = False


async def get_sentences(word: str, lang: str, to_lang: str):
    sql = """
    SELECT 
    l.id AS id, 
    l.text AS sentence, 
    l.options AS options,
    l.len_elm AS len_elm
    l.words AS words,
    t.text AS translation, 
    t.id AS to_id,
    t.options AS to_options,
    FROM content_raw.sentence_elements l
    JOIN content_raw.translation_links tl ON l.lang = tl.lang AND l.id = tl.id
    JOIN content_raw.sentences t ON tl.to_lang = t.lang AND tl.to_id = t.id
    WHERE tl.lang = %s AND tl.to_lang = %s
      AND (l.root = %s OR l.word1 = %s OR l.word2 = %s OR l.word3 = %s)
    ORDER BY l.len_elm ASC
    LIMIT 15
    """

    result = await get_query_results(sql, (lang, to_lang, word, word, word))
    # order sentences
    return result


def gen_single_choice_exercise(sentence: dict, gen_request: GenLessonRequest):
    opts = sentence.get('to_options')
    options = [Options(option=option, is_correct=False) for option in opts]
    options.append(Options(option=sentence.get('translation'), is_correct=True))
    random.shuffle(options)
    exercise = Exercise(
        exercise_type = 'single_choice',
        sentence = sentence.get('sentence'),
        sentence_id = sentence.get('id'),
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def gen_single_choice_reversed(sentence: dict, gen_request: GenLessonRequest):
    opts = sentence.get('options')
    options = [Options(option=option, is_correct=False) for option in opts]
    options.append(Options(option=sentence.get('sentence'), is_correct=True))
    random.shuffle(options)
    exercise = Exercise(
        exercise_type = 'single_choice_reversed',
        sentence = sentence.get('translation'),
        sentence_id = sentence.get('id'),
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def gen_multiple_choice_exercise(sentence: dict, gen_request: GenLessonRequest):
    pass

def gen_memory_game_exercise(sentence: dict, gen_request: GenLessonRequest):
    pass

def gen_letter_in_words_exercise(sentence: dict, gen_request: GenLessonRequest):
    pass

def gen_identify_words_in_speech_exercise(sentence: dict, gen_request: GenLessonRequest):
    words = sentence.get('words')
    words_not_in_sentence = list(set(gen_request.words_so_far) - set(words))
    words_not_in_sentence = random.choices(words_not_in_sentence, k=4)
    words_in_sentence = set(random.choices(words, k=2) + [gen_request.word])
    options = [Options(option=word, is_correct=word in words_in_sentence) for word in words_not_in_sentence]
    for word in words_in_sentence:
        options.append(Options(option=word, is_correct=True))
    exercise = Exercise(
        exercise_type = 'identify_words_in_speech',
        sentence = sentence.get('sentence'),
        sentence_id = sentence.get('id'),
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def gen_type_question_exercise(sentence: dict, gen_request: GenLessonRequest):
    pass



async def get_exercises(sentences: list[dict], gen_request: GenLessonRequest):
    exercises = []
    i = 0
    for sentence in sentences:
        i +=1
        exercises.append(gen_single_choice_exercise(sentence, gen_request, i))
        if i %3 == 0:
            break
        if i %5 == 0:
            exercises.append(gen_multiple_choice_exercise(sentence, gen_request, i))
        if i %7 == 0:
            exercises.append(gen_memory_game_exercise(sentence, gen_request, i))
        if i %11 == 0:
            exercises.append(gen_letter_in_words_exercise(sentence, gen_request, i))
        if i %13 == 0:
            exercises.append(gen_identify_words_in_speech_exercise(sentence, gen_request, i))
        if i %17 == 0:
    return exercises

@router.post("/lesson")
async def gen_lesson(request: GenLessonRequest):
    """Generate a lesson for a word
    1. get a list of sentences
    2. select sentences by 
    a. length
    b. words so far
    3. handle duplicate sentences   
    """
    sentences = await get_sentences(request.word, request.lang, request.to_lang)
    exercises = await get_exercises(sentences, request)
    return exercises


