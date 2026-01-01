from pydantic import BaseModel
from typing import Optional

from models.enums import ModeEnum, LevelEnum, CurrentPracticeEnum
from utils.scale import scale
from models.modes import PracticeMode

   
#when changing this class, we need to change the db table
class UserVocab(BaseModel):
    user_id: str
    customer_id: str = 'polyglots'
    lang: str
    to_lang: str = ""
    last_mode: PracticeMode = PracticeMode.step
    show_text: bool = False
    auto_play: bool = False
    reverse_mode: bool = False
    evaluate_mode: bool = False
    evaluate_count: int = 0
    configs:Optional[dict] = None # extra config fields
    mark : Optional[float] = 5.0
    last_step: str = "5"
    last_tag: str = ""
    current_practice_type:CurrentPracticeEnum  = CurrentPracticeEnum.step
    current_practice_id:str = "6"
    current_branch_key:str = ""


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "customer_id": self.customer_id,
            "lang": self.lang,
            "to_lang": self.to_lang,
            "last_mode": self.last_mode.value,
            "show_text": self.show_text,
            "auto_play": self.auto_play,
            "reverse_mode": self.reverse_mode,
            "evaluate_mode": self.evaluate_mode,
            "evaluate_count": self.evaluate_count,
            "last_step": self.last_step,
            "last_tag": self.last_tag,
            "current_practice_type": self.current_practice_type.value,
            "current_practice_id": self.current_practice_id,
        }

    
    def max_word_count(self):
        return scale(self.mark, 0.3, 1.0, 3, 25)
    
    def min_mark_practice(self):
        return scale(self.mark, 0.3, 1.0, 4.0, 1.0)
    
    def min_mark_refresh(self):
        return scale(self.mark, 0.3, 1.0, 6.0, 2.0)
    
    def refresh_hours_back(self):
        return scale(self.mark, 0.3, 1.0, 4, 168)

    def number_of_words(self):
        return scale(self.mark, 0.3, 1.0, 1, 4)
    
    def is_step_completed(self, step:int):
        # how to define a step as completed?
        pass
    def get_next_mode(self):
        return  PracticeMode.get_next_mode(self.last_mode) 
    def get_schema(self):
        return f"{self.customer_id}_quiz"
    def get_user_schema(self):
        return f"{self.customer_id}_users"