from pydantic import BaseModel

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
