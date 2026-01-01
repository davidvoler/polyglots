from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional, List
import random

from enum import Enum


class Mode(Enum):
    branch = 'branch'
    refresh = 'refresh'
    mixed = 'mixed'



class History(BaseModel):
    score: float = 0.0
    times: int = 0
    avg_score: float = 0.0
    first_time: datetime = datetime.now()
    last_time: datetime = datetime.now()

class Branch(BaseModel):
    key: str = ''
    word: str = ''
    level: int = 0
    times: int = 0
    avg_score: float = 0.0
    first_time: datetime = datetime.now()
    last_time: datetime = datetime.now()


class UserHistory(BaseModel):
    words: Dict[str, History] = {}
    parts: Dict[str, History] = {}
    branches: Dict[str, Branch] = {}
    main_branches: Dict[str, Branch] = {}
    daily_score: Dict[str, float] = {}
    weekly_score: Dict[str, float] = {}
    monthly_score: Dict[str, float] = {}
    refresh_scores: List[History] = {}
    modes: Dict[int, Mode] = {}
    last_time:datetime = datetime.now()
    first_time:datetime = datetime.now()
    current_parts: List[int] = []
    current_branch: str = ''
    current_branch_idx: int = 0
    current_main_branch: str = ''

    def update_score(self, score:float, branch_key:str='', referesh_days:int=-1, words:list =[]):
        pass

    def get_branch_avg_score(self):
        branch = self.branches.get(self.current_branch, None) 
        if branch:
            return branch.avg_score
        return 0.0

    def get_refresh_avg_score(self):
        try:
            refresh_scores = self.refresh_scores[-1] 
        except:
            refresh_scores = None
        if refresh_scores:
            return refresh_scores.avg_score
        return 0.0

    def get_main_branch_avg_score(self):
        main_branch = self.main_branches.get(self.current_main_branch, None) 
        if main_branch:
            return main_branch.avg_score
        return 0.0

    def get_refresh_parts(self, score:float, score_factor:float, randomize:bool=True):
        parts = []
        n = datetime.now()
        for part_id, part in self.parts:
            if part.score <  score + (n - part.last_time).days * score_factor < part.score:
                parts.append(part_id)
        if randomize:
            random.shuffle(parts)
        return parts[:10]

    def get_branch_parts(self, max_score:float, randomize:bool=True):
        parts = []
        current_branch = self.branches.get(self.current_branch, None)
        if not:
            branch_parts = current_branch.parts
        else:
            self.get_next_branch()

        #prefer new parts or parts with score less than max_score
        for p in self.branch_parts:
            if p not in self.parts.keys():
                parts.append(p)
            elif self.parts[p].score < max_score:
                parts.append(p)
        # add parts even if they are not new or score is higher than max_score
        if len(parts) < 10:
            for p in branch_parts:
                if p not in parts:
                    parts.append(p)
        parts = parts[:10]
        if randomize:
            random.shuffle(parts)
        return parts[:10]

    def get_parts(self, randomize:bool=False):
        """
        get the parts for the current mode
        if mode does not have enough parts, add parts from other modes
        """
        max_score = self.user_params.max_score
        score_factor = self.user_params.score_factor
        parts = []
        if len(self.modes) == 0:
            self.gen_modes()
        mode = self.modes[-1]
        if mode == Mode.branch:
            parts = self.get_branch_parts(max_score, randomize)
            if len(parts) < 10:
                # add refresh parts
                refresh_parts = self.get_refresh_parts(max_score, score_factor, randomize)
                return parts + refresh_parts[:10-len(parts)]
        elif mode == 'refresh':
            parts = self.get_refresh_parts(max_score, score_factor, randomize)
            if len(parts) < 10:
                branch_parts = self.get_branch_parts(max_score, randomize)
                if len(branch_parts) < 10:
                    self.get_next_branch_parts()
                return parts + branch_parts[:10-len(parts)]
        return parts