from pydantic import BaseModel
from datetime import datetime


class Question(BaseModel):
    id: int = 0
    word: str = ''
    lang: str
    to_lang:str
    to_id: int = 0
    sentence: str = ''
    translation:str = ''
    options:list[str] = []
    explain:str = ''
    question_type: str = ''


class Lesson(BaseModel):
    name: str = ''
    words: list[str] = []


class Module(BaseModel):
    name: str = ''
    words: list[str] = []
