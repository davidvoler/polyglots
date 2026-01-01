from pydantic import BaseModel
from enum import Enum 



class ElementType(str, Enum):
    word = 'word'
    part = 'part'
    line = 'line'
    dialogue = 'dialogue'
    phrase = 'phrase'

class PreviewType(str, Enum):
    step = 'step'
    tag = 'tag'
    dialogue = 'dialogue'


class PreviewRequest(BaseModel):
    lang: str
    to_lang: str
    user_id: str
    customer_id: str = 'polyglots'
    

class UserStatusResponse(BaseModel):
    lang: str=""
    to_lang: str=""
    user_id: str=""
    practice_id: str=""
    practice_type: str =""
    completed: int =0
    remaining: int = 0
    accuracy: int = 0
    times: int = 0
    minutes: int = 0





class Preview(BaseModel):
    preview_type : PreviewType
    preview_id: str = ''
    tag: str = ''
    header: str = ''
    words: list = []
    parts: list = []
    ul_words: list = []
    ul_parts: list = []
    ul_header: str = ''
    new: int = 0
    in_progress: int = 0
    done: int = 0
    completed: bool = False

