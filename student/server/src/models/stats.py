from pydantic import BaseModel


class Stats(BaseModel):
    user_id: str
    lang: str
    to_lang: str
    course_id: int
    lessons: int = 0
    exercises: int = 0
    words: int= 0
    sentences: int = 0
    alphabet: int = 0

class StatsRequest(BaseModel):
    user_id: str
    lang: str
    to_lang: str