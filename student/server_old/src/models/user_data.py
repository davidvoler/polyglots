from pydantic import BaseModel
from datetime import datetime, timedelta
from models.quiz import Branch
from utils.quiz_tatoeba_cache.branch_utils import get_next_branch
from models.branch import Branch


MAX_BRANCH_TIMES = 60

class UserScores(BaseModel):
    score: float = 5.0
    times: int = 30
    last_seen_days: int = 0



def create_user_scores(score_start: float = 5.0, times_start: int = 30) -> list[UserScores]:
    u_scores = []
    times = times_start
    score = score_start
    for days in [2, 7, 14, 30, 60]:
        times = times_start +3
        score = score_start +0.3    
        u_scores.append(UserScores(
            score=score, 
            times=times, 
            last_seen_days=days))


class UserMarks(BaseModel):
    mark: float = 0.0
    times: int = 0
    avg_mark: float = 0.0
    branch_mark: float = 0.0
    branch_times: int = 0
    avg_branch_mark: float = 0.0
    main_branch_mark: float = 0.0
    main_branch_times: int = 0
    avg_main_branch_mark: float = 0.0
    user_scores: list[UserScores] = []


    def calc_marks(self, mark: float, times: int, branch: Branch=None, main_branch: Branch=None):
        self.mark = mark
        self.times = times
        if branch:
            self.branch_mark = branch.mark
            self.branch_times =  branch.times
            if self.branch_times > 0:
                self.avg_branch_mark = self.branch_mark / self.branch_times
        if main_branch:
            self.main_branch_mark = main_branch.mark
            self.main_branch_times = main_branch.times
            if self.main_branch_times > 0:
                self.avg_main_branch_mark = self.main_branch_mark / self.main_branch_times

    def make_a_decision(self):
        if self.branch_mark < 0.3:
            if self.branch_times > MAX_BRANCH_TIMES:
                return True
            else:
                return False
        if self.branch_mark >= 0.3:
            pass
        elif self.branch_mark > 0.5:
            pass
        elif self.branch_mark > 0.7:
            pass
        elif self.branch_mark > 0.85:
            pass
        elif self.branch_mark > 0.9:
            pass
        else:
            pass

#when changing this class, we need to change the db table
class UserData(BaseModel):
    user_id: str
    lang: str
    parts_marks: map = {}
    parts_times: map = {}
    parts_last: map = {}
    parts_first: map = {}
    branches: map = {}
    main_branches: map = {}
    words_marks: map = {}
    words_times: map = {}
    words_last: map = {}
    words_first: map = {}
    current_branch: Branch = None
    main_branch: Branch = None
    mark: float = 0.0
    times: int = 0
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
    
    def get_users_marks(self):
        user_marks = UserMarks()
        user_marks.calc_marks(self.mark, self.times, self.current_branch, self.main_branch)
        return user_marks





    
    def select_next_branch(self):
        if self.main_branch:
            if self.root_branch_times > 0:
                avg_mark = self.current_branch.mark / self.current_branch.times
                if avg_mark > 0.5:
                    # stay on main branch
                    branch = get_next_branch(self.lang, self.root_branch_word, self.words_marks.keys(), self.current_branch_parts, self.current_branch_times)
                else:
                    # move to a new branch
                    branch = get_next_branch(self.lang, self.root_branch_word, self.words_marks.keys(), self.current_branch_parts, self.current_branch_times)
        else:
            branch = get_next_branch(self.lang, self.root_branch_word, self.words_marks.keys(), self.current_branch_parts, self.current_branch_times)
        
        if self.main_branche.word != branch.word:
            #remove the old main branch - save ti to history
            # TODO: if it already exists merge it 
            self.root_branches[self.main_branch.get_main_branch_key()] = self.main_branch
            self.main_branch = branch
        #TODO: in case the branch we got was already in the history, we need to merge it
        self.current_branch = branch
        

    def get_branch_parts(self, max_times:int, max_score:float):
        """
        get the parts that are in the current branch
        remove parts that have been answered more than max_times or have a higher score 
        return the parts
        """
        branch_parts = self.current_branch.parts
        remove_high_score_parts = [p for p in branch_parts if self.parts_marks[p.id] > max_score]
        parts = list(set(branch_parts) - set(remove_high_score_parts))
        return parts



    def get_refresh_parts(self, max_last:timedelta, max_score:float, max_times:int):
        """
        get the parts that have not been answered in the last max_last days
        remove parts that have been answered more than max_times or have a higher score 
        return the parts
        """
        parts = [p for p in self.parts_last if p.last_time < max_last]
        return parts

    def get_reapet_parts(self):
        pass

