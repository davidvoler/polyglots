from pydantic import BaseModel
from enum import Enum


class QuizType(Enum):
    lesson = "lesson"
    refresh_module = "refresh_module"
    refresh_course = "refresh_course"
    refresh_all = "refresh_all"


class QuizRequest(BaseModel):
    lang: str = ''
    to_lang: str = ''
    user_id: str = ''
    quiz_type: QuizType = QuizType.lesson
    course_id: int = 0
    lesson_id: int = 0
    module_id: int = 0


class Option(BaseModel):
    option: str
    correct: bool = False
    selected: bool = False


class Sentence(BaseModel):
    sentence: str
    options: list[Option] = []
    words: list = []
    sentence_id: str
    sound: str = ''
    annotated_sentence: dict = {}
    exercise_type: str = 'sentence_single_choice'


class Quiz(BaseModel):
    lang: str = ''
    to_lang: str = ''
    user_id: str = ''
    quiz_type: QuizType = QuizType.lesson
    course_id: int = 0
    module_id: int = 0
    lesson_id: int = 0
    sentences: list[Sentence] = []
