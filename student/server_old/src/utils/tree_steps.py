from pydantic import BaseModel


class SubStepInfo(BaseModel):
    user_id: str
    sub_step: int
    ratio: float
    max_w_count: int 



class StepInfo(BaseModel):
    user_id: str
    step: int
    ratio: float = 0.4
    sub_steps: list[SubStepInfo] = []
    def step_count(self):
        return len(self.sub_steps)
    





class UserStepInfo(BaseModel):
    lang: str
    to_lang: str
    step: int
    sub_step: int
    user_words: list = []
    ratio: float = 0.4
    ratio_step: int = 0.1
    ratio_sub_step: int = 0.1
    key_words_step: list  = []
    key_words_sub_step: list = []
    sub_steps: int = 0

    def min_w_count(self):
        return 3
    def max_w_count(self): #should be calculated by ratio
        return 10
    def max_key_words(self): #should be calculated by ratio
        return 20


async def get_tree_step(lang, to_lang, step, sub_step):
    sql = """select * from tatoeba.tree_steps where lang = %s and to_lang = %s and step = %s and sub_step = %s"""


async def get_next_step(lang, to_lang, step, sub_step, user_words:list):
    pass

async def select_branch(lang, to_lang,step, sub_step):
    pass



