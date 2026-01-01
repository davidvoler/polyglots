from pydantic import BaseModel
from models.modes import PracticeMode


class Results(BaseModel):
    user_id:str
    lang:str
    customer_id:str = 'polyglots'
    part_id:str = ''
    dialogue_id:str = ''
    dialogue_line:str = ''
    step:str = ''
    attempts:int = 0
    words:list = []
    structure: bool = False
    tag: str = ''
    corpus: str = ''
    branch_word: str = ''
    branch_key: str = ''
    wcount: int = 0
    answer_delay_ms: int = 0
    play_times: int = 0
    branch_key: str = ''


    def get_schema(self):
        return f"{self.customer_id}_quiz"
    def get_user_schema(self):
        return f"{self.customer_id}_users"

    def _get_results_fields(self):
        return ','.join(['user_id', 'lang', 'part_id', 'dialogue_id', 'dialogue_line', 'step', 'last_time'])



class ResultsBranch(BaseModel):
    user_id:str
    lang:str
    customer_id:str = 'Tatoeba'
    part_id:int = 0
    brnach_key: str = ''
    branch_word: str = ''
    attempts:int = 0
    play_times:int = 0
    answer_delay_ms:int = 0
    words:list = []

    
    def get_schema(self):
        return f"{self.customer_id}_quiz"
    def get_user_schema(self):
        return f"{self.customer_id}_users"

    def _get_results_fields(self):
        return ','.join(['user_id', 'lang', 'part_id', 'dialogue_id', 'dialogue_line', 'step', 'last_time'])


    
