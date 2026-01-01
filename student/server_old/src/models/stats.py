from pydantic import BaseModel
from models.enums import ModeEnum, LevelEnum

class StatsRequest(BaseModel):
    user_id: str
    lang: str
    granularity: str = 'day'
    customer_id: str = 'polyglots'


class Progress(BaseModel):
    user_id: str
    lang: str
    questions: int
    words: int
    sentences: int

class Stats(BaseModel):
    user_id: str
    lang: str
    granularity: str = 'day'
    journal:list = []
    new_items:list = []
    mastered_items:list = []
    mark: float= 0.4
    


class StatsElement(BaseModel):
    label: str
    accuracy: int = 0.0 
    new_items:int = 0
    completed_items:int = 0
    questions:int = 0


class StatsElementGraph(BaseModel):
    label: list= []
    accuracy: list = []
    new_items: list = []
    completed_items: list = []
    questions: list = []