from pydantic import BaseModel
from models.modes import PracticeMode
from typing import Optional
from datetime import datetime
from enum import Enum


class QuizType(Enum):
    lesson = "lesson"
    refresh_module = "refresh_module"
    refresh_course = "refresh_course"
    refresh_all = "refresh_all"


class QuizRequest(BaseModel):
    lang:str = ''
    to_lang:str = ''
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
    words:list = []
    sentence_id: str
    sound:str = ''
    dialogue_id: str = ''
    dialogue_line: str = ''
    translit: str|None = ''
    

class Quiz(BaseModel):
    lang:str
    to_lang:str    
    mode: PracticeMode = PracticeMode.step
    sentences: list[Sentence] = []
    practice_type: str = ''
    practice_id: str = ''
    dialogue_id: str = ''
    accuracy: float = 0.0
    reverse_mode: Optional[bool] = False
    remaining : Optional[int] = 0
    accuracy: Optional[float] = 0.0
    completed: Optional[int] = 0
    minutes: Optional[int] = 0
    times: Optional[int] = 0
    practice_times : int = 0
    practice_mark : float = 0.0
    step: Optional[int] = 3
    change_step: Optional[bool] = False  




class QuizRequestBranch(QuizRequest):
    branch_key: str = ''
    branch_word: str = ''
    branch_accuracy: int = 0
    branch_tims: int = 0
    max_wcount: int = 12
    max_level: int = 3



class Branch(QuizRequestBranch):
    lang: str = ''
    key: str = ''
    word: str = ''
    level: int = 0
    max_wcount: int = 0
    linked_words: list[str] = []
    linked_sentences: list[int] = []
    first_time: datetime = datetime.now()
    last_time: datetime = datetime.now()
    times: int = 0
    mark: float = 0.0
    
    def get_main_branch_key(self)->str:
        return f"{self.lang}:{self.word}"


