from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum, auto


class PracticeMode(Enum):
    words='words' 
    branch='step'
    refresh = 'refresh'
    repeat = 'repeat'

    def get_next_mode( current_mode):
        modes = list(PracticeMode)
        current_index = modes.index(current_mode)
        next_index = (current_index + 1) % len(modes)
        return modes[next_index]

class QuizRequestBranch(BaseModel):
    lang:str = ''
    to_lang:str = ''
    user_id: str = ''
    reversed: Optional[bool] = False
    last_mode: Optional[PracticeMode] = None
    corpus: Optional[str] = 'branches'
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

class UserCache(BaseModel):
    user_id: str = ''
    lang: str = ''
    created_at: datetime = datetime.now()
    branch_times: list[int] = []
    branch_marks: list[float] = []
    words_times: list[int] = []
    words_marks: list[float] = []
    parts_times: list[int] = []
    parts_marks: list[float] = []
    def get_key(self):
        return f"{self.user_id}:{self.lang}"
    
    



