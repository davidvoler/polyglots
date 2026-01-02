from pydantic import BaseModel


class Results(BaseModel):
    user_id:str
    sentence_id: int = 0
    exercise_id: int = 0
    letter: str = ''
    lang:str
    attempts:int = 0
    words:list = []
    answer_delay_ms: int = 0
    play_times: int = 0


