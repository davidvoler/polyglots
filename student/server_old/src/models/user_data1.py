from pydantic import BaseModel
from datetime import datetime, timedelta
from models.quiz import Branch
from utils.quiz_tatoeba_cache.branch_utils import get_next_branch
from models.branch import Branch

   
#when changing this class, we need to change the db table
class UserData(BaseModel):
    user_id: str
    lang: str
    parts_marks: map = {}
    parts_times: map = {}
    parts_last: map = {}
    parts_first: map = {}
    branches_marks: map = {}
    branches_times: map = {}
    branches_last: map = {}
    branches_first: map = {}
    words_marks: map = {}
    words_times: map = {}
    words_last: map = {}
    words_first: map = {}
    current_branch_key: str = ''
    current_branch_linked_words: list = []
    current_branch_parts: list = [] # parts that are in the current branch
    current_branch_times: int = 0
    current_branch_mark: float = 0.0
    mark: float = 0.0
    times: int = 0
    root_branch_word: str = ''
    root_branch_mark: float = 0.0
    root_branch_times: int = 0
    root_branch_first: datetime = datetime.now()
    last_reset: datetime = datetime.now()

    
    def get_parts_mark_limit(self,max_mark:float , min_mark:float= -30):
        res = []
        for part_id, mark in self.parts_marks.items():
            if mark < max_mark and mark > min_mark:
                res.append(part_id)
        return res
    
    def get_words_limit(self,max_mark:float , min_mark:float= -30):
        res = []
        for part_id, mark in self.words_marks.items():
            if mark < max_mark and mark > min_mark:
                res.append(part_id)
        return res

    def get_branches_limit(self,max_mark:float , min_mark:float= -30):
        res = []
        for part_id, mark in self.branches_marks.items():
            if mark < max_mark and mark > min_mark:
                res.append(part_id)
        return res
    def get_repeat_parts(self,max_times:int , min_times:int= 1):
        pass
    def get_refresh_parts(self,max_last:timedelta, min_last:timedelta= timedelta(days=30)):
        pass
    def get_current_branch_parts(self):
        # get the parts that are in the current branch
        # remove parts that have been answered more than max_times or have a higher score 
        return self.current_branch_parts
    def select_next_branch(self):
        if self.root_branch_word:
            if self.root_branch_times > 0:
                avg_mark = self.root_branch_mark / self.root_branch_times
                if avg_mark > 0.5:
                    # stay on main branch
                    branch = get_next_branch(self.lang, self.root_branch_word, self.words_marks.keys(), self.current_branch_parts, self.current_branch_times)
                else:
                    # move to a new branch
                    branch = get_next_branch(self.lang, self.root_branch_word, self.words_marks.keys(), self.current_branch_parts, self.current_branch_times)
        else:
            branch = get_next_branch(self.lang, self.root_branch_word, self.words_marks.keys(), self.current_branch_parts, self.current_branch_times)
        if self.root_branch_word != branch.word:
            self.root_branch_word = branch.word
            self.root_branch_mark = 0.0
            self.root_branch_times = 0
            self.root_branch_first = datetime.now()
        self.current_branch_key = branch.key
        self.current_branch_times = 0
        self.current_branch_mark = 0.0
        self.current_branch_parts = branch.linked_sentences
        self.current_branch_linked_words = branch.linked_words
        


