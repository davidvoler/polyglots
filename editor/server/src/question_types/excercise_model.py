from pydantic import BaseModel

class ExerciseModel(BaseModel):
    lesson_id: int
    module_id: int
    course_id: int
    weight: int = 0
    exercise_type: str
    lang: str = ''
    to_lang: str = ''
    title: str
    instruction: str
    sentence: str
    extra_data: dict = {}
    word: str = ''
    letter: str = ''
    verb: str = ''
    verb_lemma: str = ''
    noun: str = ''
    adjective: str = ''
    auxiliary: str = ''
