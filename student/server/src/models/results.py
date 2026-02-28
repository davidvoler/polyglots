from pydantic import BaseModel


class Results(BaseModel):
    user_id: str
    lang: str = ''
    to_lang: str = ''
    exercise_id: int = 0
    lesson_id: int = 0
    module_id: int = 0
    course_id: int = 0
    exercise_type: str = ''
    correct: bool = False
    attempts: int = 0
    answer_delay_ms: int = 0
