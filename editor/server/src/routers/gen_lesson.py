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
    sentence_id: int = 0
    to_sentence_id: int = 0
    incomplete_sentence: str = ''
    voice: str = ''
class GenLessonRequest(BaseModel):
    word: str
    lang: str
    to_lang: str
    words_so_far: list[str]
    words_so_far_in_sentences: list[str]
    letters_so_far: list[any]
    is_alphabet: bool = False

class SelectSentencesRequest(BaseModel):
    words: list[str]
    lang: str
    to_lang: str
    words_so_far: list[str]
    words_so_far_in_sentences: list[str]
    letters_so_far: list[any]
    is_alphabet: bool = False

class SelectSentencesItem(BaseModel):
    id: int = 0
    to_id: int = 0
    sentence: str = ''
    translation: str = ''
    to_options: list[str] = []
    len_elm: int = 0
    selected: bool = True
    duplicate: bool = False
    single_choice: bool = True
    identify_words: bool = False
    type_question: bool = False
    single_choice_reversed: bool = False

class SelectSentencesResponse(BaseModel):
    sentences: dict[str, list[SelectSentencesItem]]

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
    ORDER BY l.len_elm ASC l.sentence ASC
    LIMIT 30
    """
    result = await get_query_results(sql, (lang, to_lang, word, word, word))
    # order sentences
    sentences_ids = {}
    for row in result:
        sid = row.get('id')
        if sid not in sentences_ids:
            sentences_ids[sid] = 1
        else:
            sentences_ids[sid] += 1
    sentences = []
    for row in result:
        sid = row.get('id')
        if sentences_ids[sid] > 1:
            row['duplicate'] = True
        sentences.append(SelectSentencesItem(**row))
    return sentences


def gen_single_choice_exercise(sentence: dict, voice: str, gen_request: GenLessonRequest):
    opts = sentence.get('to_options')
    options = [Options(option=option, is_correct=False) for option in opts]
    options.append(Options(option=sentence.get('translation'), is_correct=True))
    random.shuffle(options)
    exercise = Exercise(
        exercise_type = 'single_choice',
        sentence = sentence.get('sentence'),
        voice = voice,
        sentence_id = sentence.get('id'),
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def gen_single_choice_reversed(sentence: dict, voice: str, gen_request: GenLessonRequest):
    opts = sentence.get('options')
    options = [Options(option=option, is_correct=False) for option in opts]
    options.append(Options(option=sentence.get('sentence'), is_correct=True))
    random.shuffle(options)
    exercise = Exercise(
        exercise_type = 'single_choice_reversed',
        sentence = sentence.get('translation'),
        voice = voice,
        sentence_id = sentence.get('id'),
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def gen_multiple_choice_exercise(sentence: dict, gen_request: GenLessonRequest):
    pass

def gen_identify_words_in_speech_exercise(sentence: dict, voice: str, gen_request: GenLessonRequest):
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
        voice = voice,
        sentence_id = sentence.get('id'),
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def gen_type_question_exercise(sentence: dict, voice: str, gen_request: GenLessonRequest):
    words = sentence.get('words')
    sentence = sentence.get('sentence')
    for w in words:
        if w not in sentence:
            sentence = sentence.replace(w, '__')
    words_so_far = gen_request.words_so_far
    wrong_words = list(set(words_so_far) - set(words))
    wrong_words = random.choices(wrong_words, k=4)
    options  = [Options(option=word, is_correct=False) for word in wrong_words]
    for word in words:
        options.append(Options(option=word, is_correct=True))
    exercise = Exercise(
        exercise_type = 'type_question',
        sentence = sentence.get('sentence'),
        voice = voice,
        sentence_id = sentence.get('id'),   
        to_sentence_id = sentence.get('to_id'),
        options = options,
    )
    return exercise

def get_exercises(sentences: list[dict], recordings: dict, gen_request: GenLessonRequest):
    exercises = []
    i = 0
    for sentence in sentences:
        i +=1
        voice = recordings.get(sentence.get('id'))
        exercises.append(gen_single_choice_exercise(sentence, voice, gen_request))
        if i %3 == 0:
            if voice:
                exercises.append(gen_identify_words_in_speech_exercise(sentence, voice, gen_request))
        if i %4 == 0:
            if len(gen_request.words_so_far) > 6:
                exercises.append(gen_type_question_exercise(sentence, voice, gen_request))
        if i %5 == 0:
            if len(gen_request.words_so_far) > 6:
                exercises.append(gen_single_choice_reversed(sentence, voice, gen_request))
    return exercises

async def get_recordings(sentences: list[dict], lang: str):
    ids = [sentence.get('id') for sentence in sentences]
    placeholders = ','.join(['%s'] * len(ids))
    sql = """
    SELECT 
    recording, audio_engine
    FROM content_raw.audio
    WHERE r.lang = %s 
    AND id IN ({placeholders})
    """
    results = await get_query_results(sql, (lang, *ids))
    recordings = {}
    for result in results:
        recordings[result.get('id')] = result.get('recording')
    return recordings


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
    recordings = await get_recordings(sentences, request.lang)
    exercises = get_exercises(sentences, recordings, request)
    return exercises



@router.post("/select_sentences")
async def select_sentences(request: SelectSentencesRequest) -> SelectSentencesResponse:
    sentences = {}
    for word in request.words:
        sentences[word] = await get_sentences(word, request.lang, request.to_lang)
    return SelectSentencesResponse(sentences=sentences)