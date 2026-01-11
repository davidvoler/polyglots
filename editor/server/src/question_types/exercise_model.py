from pydantic import BaseModel
import json 
from utils.db import run_query


class ExerciseModel(BaseModel):
    lesson_id: int = 0
    module_id: int = 0
    course_id: int = 0
    weight: int = 0
    exercise_type: str = ''
    lang: str = ''
    to_lang: str = ''
    title: str = ''
    instruction: str = ''
    sentence: str = ''
    extra_data: dict = {}
    annotated_sentence: list[dict] = []
    ab_type: str = ''
    word: str = ''
    letter: str = ''
    verb: str = ''
    verb_lemma: str = ''
    noun: str = ''
    adjective: str = ''
    auxiliary: str = ''
    sentence_id: int = 0
    to_sentence_id: int = 0
    correct_options: list[str] = []
    wrong_options: list[str] = []
    audio_link: str = ''


async def save_exercise_new_format(exercise: ExerciseModel):
    sql = """
    INSERT INTO content.exercise(lesson_id, module_id, course_id, exercise_type, lang, to_lang, title, instruction, sentence, extra_data, annotated_sentence, word, letter, verb, 
    verb_lemma, noun, adjective, auxiliary, ab_type, sentence_id, to_sentence_id, correct_options, wrong_options, audio_link)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    await run_query(sql, (exercise.lesson_id, exercise.module_id, exercise.course_id, exercise.exercise_type, exercise.lang, exercise.to_lang, exercise.title, exercise.instruction, exercise.sentence,
    json.dumps(exercise.extra_data), json.dumps(exercise.annotated_sentence), exercise.word, exercise.letter, exercise.verb, exercise.verb_lemma, exercise.noun, exercise.adjective, exercise.auxiliary, 
    exercise.ab_type, exercise.sentence_id, exercise.to_sentence_id, exercise.correct_options, exercise.wrong_options, exercise.audio_link))
