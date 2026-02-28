from pydantic import BaseModel


class Stats(BaseModel):
    user_id: str
    lang: str
    to_lang: str
    course_id: int = 0
    lessons: int = 0
    exercises: int = 0
    correct: int = 0
    total: int = 0


class StatsRequest(BaseModel):
    user_id: str
    lang: str
    to_lang: str
    course_id: int = 0
