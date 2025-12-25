from pydantic import BaseModel


class WordSelect(BaseModel):
    lang: str
    word:str = ''
    pos: str = ''
    max_wcount: int = 0
    min_wcount: int= 0
    sentences_count: int = 0
    root_count: int = 0
    def key(self):
        return f"{self.lang}-{self.pos} "

class ModuleWords(BaseModel):
    name: str = ''
    num: int = 0
    words:list[WordSelect] = []
    word_count:int = 0



class WordSelectRequest(BaseModel):
    lang:str
    words_per_modules: int = 5
    ratio_increase:float = 0.08
    