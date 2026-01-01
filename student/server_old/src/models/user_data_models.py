from pydantic import BaseModel
from datetime import datetime, timedelta
from enums import Enum
import random
from models.app_params import AppParams, get_app_params


REFRESH_DAYS = [(0,10),  (2, 10),  (7, 6),  (14, 6),  (21, 5),  (30, 5),  (60, 4),  (90, 4),  (120, 3)]



    


class UserParams(BaseModel):
    branch_times: int
    main_branch_times: int
    refresh_score_factor: float
    refresh_days: list[int]
    level: int 
    wcount: int 
    avg_score: float 
    created_at: datetime
    last_update: datetime
    test_mode: bool = False


class Results(BaseModel):
    user_id: str
    lang: str
    part_id: int
    branch_key: str
    branch_word: str
    wcount: int
    answer_delay_ms: int
    play_times: int
    attempts: int
    refresh_level: int = 0
    mode: str
    score: float = 0.0
    
    def calc_score(self):
        play_times_score = 0.0
        if self.play_times <= 1:
            play_times_score = 0.05
        elif self.play_times == 2:
            play_times_score = -0.02
        else:
            play_times_score = -0.05
        answer_delay_score = 0.0
        if self.answer_delay_ms < 2500:
            answer_delay_score = 0.05
        elif self.answer_delay_ms < 3500:
            answer_delay_score = 0.02
        else:
            answer_delay_score = -0.05
        
        if self.attempts == 1:
            self.score = 1.0
        elif self.attempts == 2:
            self.score = -0.75
        else:
            self.score = -0.9
        self.score += play_times_score + answer_delay_score

class UserScoreHistory(BaseModel):
    score: float = 0.0
    times: int = 0
    avg_score: float = 0.0

class RefreshScore(BaseModel):
    score: float = 5.0
    max_times: int = 300

class Branch(BaseModel):
    key: str = ''
    word: str = ''
    level: int = 0
    max_wcount: int = 0
    branch_score: int = 0
    branch_tims: int = 0
    linked_words: list[str] = []
    linked_sentences: list[int] = []



class UserRepeatScores(BaseModel):
    score: float = 5.0
    times: int = 30
    days: int = 0
    last_seen_days: int = 0


class UserPart(BaseModel):
    score: float = 0.0
    times: int = 0
    w_count: int = 0
    last_time: datetime = datetime.now()
    first_time: datetime = datetime.now()
     
class UserWord(BaseModel):
    score: float = 0.0
    times: int = 0
    last_time: datetime = datetime.now()
    first_time: datetime = datetime.now()


class RefreshScore(BaseModel):
    score: float = 0.0
    times: int = 0
    last_time: datetime = datetime.now()
    first_time: datetime = datetime.now()


class Stats(BaseModel):
    score: float = 0.0
    times: int = 0
    last_time: datetime = datetime.now()
    first_time: datetime = datetime.now()

class UserData(BaseModel):
    user_id: str
    lang: str
    parts: map = {}
    words: map = {}
    branches: map = {}
    main_branches: map = {}
    current_branch: Branch = None
    current_main_branch: Branch = None
    score: float = 0.0
    times: int = 0
    last_reset: datetime = datetime.now()
    user_repeat_scores: list[UserRepeatScores] = []
    created_at: datetime = datetime.now()
    modes = []
    modes_score: list[RefreshScore] = []
    evaluate_mode: bool = False # when user is in evaluate mode - we offer a mixed level quiz - some hard some simple
    user_score_history: list[UserScoreHistory] = []
    score_since_evaluate: float = 0.0
    times_since_evaluate: int = 0
    score_refresh: float = 0.0
    times_refresh: int = 0
    user_params: UserParams = UserParams()
    app_params: AppParams = get_app_params()
    results: list[Results] = []
    refresh_scores: map = {}
    day_stats: map = {}
    week_stats: map = {}
    month_stats: map = {}
    


    def get_last_avg_score(self, count:int = 10):
        return sum(self.user_score_history[-count:]) / count, count

    def update_stats(self):
        pass
    def get_stats(self):
        pass


    def change_users_params(self):
        avg, count = self.get_last_avg_score()
        change_avg = 0.0
        if count >= 5:
            change_avg = avg - user_score.avg_score
        if change_avg > 0.2:
            # TODO change user's params based on  
            pass 

    def evaluate(self):
        if self.times_since_evaluate >= self.app_params.evaluate_times:
            try:
                user_score = UserScoreHistory(
                    score=self.score_since_evaluate, 
                    times=self.times_since_evaluate, 
                    avg_score=self.score_since_evaluate/self.times_since_evaluate)
                self.user_score_history.insert(0, user_score)
                self.times_since_evaluate = 0
                self.score_since_evaluate =0.0
                self.change_users_params()
            except Exception as e:
                print(e)
    
    
    def save_results(self):
        for results in self.results:
            results.calc_score()
            if results.branch_key:
                self.current_branch.score += results.score
                self.current_branch.times += 1
                self.main_branch.score += results.score
                self.main_branch.times += 1
            elif results.refresh_level > 0:
                if results.refresh_level not in self.refresh_scores:
                    ref_score = RefreshScore(
                    )
                else:
                    ref_score = self.refresh_scores[results.refresh_level]
                ref_score.score += results.score
                ref_score.times += 1
                ref_score.last_time = datetime.now()
                self.refresh_scores[results.refresh_level] = ref_score
            for w in results.words:
                if w not in self.words:
                    self.words[w] = UserWord()
                self.words[w].score += results.score
                self.words[w].times += 1
                self.words[w].last_time = datetime.now()
            if results.part_id not in self.parts:
                self.parts[results.part_id] = UserPart()
            self.parts[results.part_id].score += results.score
            self.parts[results.part_id].times += 1
            self.parts[results.part_id].last_seen = datetime.now()
            self.score += results.score
            self.score_since_evaluate += results.score
            self.times += 1
            self.times_since_evaluate+=1
        self.results = []
        self.update_stats()

    def create_user_scores(self, score_start: float = 5.0, times_start: int = 30) -> list[UserRepeatScores]:
        u_scores = []
        times = times_start
        score = score_start
        for days in [0, 2, 7, 14, 30, 90]:
            times = times_start +3
            score = score_start +0.3    
            u_scores.append(UserRepeatScores(
                score=score, 
                times=times, 
                last_seen_days=days))    
        self.user_repeat_scores = u_scores

    def get_avg_score(self):
        if self.times_since_evaluate > 0:
            return self.score_since_evaluate / self.times_since_evaluate
        else:
            return 0.0

    def get_users_modes(self):
        days_since_start = (datetime.now() - self.created_at).days
        modes = []
        refresh_score = []
        score_factor = self.app_params.get_refresh_score_factor(self.get_avg_score())
        score = self.app_params.get_score(self.get_avg_score())
        max_time = self.app_params.get_max_time(self.get_avg_score())
        max_time_factor = self.app_params.get_max_time_factor(self.get_avg_score())
        i = 0
        for days in self.app_params.refresh_days_range:
            if days_since_start > days[0]:
                modes.extend(days[1]*[days[0]])
                refresh_score.append(RefreshScore(
                    score=score + i*score_factor,
                    times=max_time + i*max_time_factor,
                ))
                i+=1
        random.shuffle(modes)
        self.modes = modes

    def get_mode(self):
        if len(self.modes) == 0:
            self.get_users_modes()
        return self.modes.pop(0)

    def get_branch_parts(self):
        if not self.current_branch:
            self.get_branch()
        # remove_high_score_parts  
        parts = []
        for p in self.current_branch.parts:
            if p not in self.parts.keys()
                parts.append(self.parts[p].score)
            elif self.parts[p].score < self.user_params.max_score:
                parts.append(p)
        #TODO: handle when not enough parts
        return parts          

    def get_refresh_parts(self, mode: int):
        practice = self.user_repeat_scores[mode]
        dt = datetime.now() - timedelta(days=practice.days)
        parts = [part.id for part in self.parts 
            if part.last_time < dt 
            and part.times < practice.times and part.score < practice.score]
        #TODO: handle when not enough parts
        return parts

    def get_parts(self, mode: int):
        if mode == 0:
            parts = self.get_branch_parts()      
        else:
            parts = self.get_refresh_parts(mode)
        return parts

    def get_practice_parts(self):
        mode = self.get_mode()
        if mode == 0:
            return self.get_branch_parts()
        elif mode == 1:
            return self.get_refresh_parts(mode)

def create_user_data(user_id: str, lang: str) -> UserData:
    # create starter branch and main branch
    user_data = UserData(user_id=user_id, lang=lang)
    user_data.create_user_scores()
    return user_data





## alternative to the above funtion
# when we have results from user only save them to user_data as is 
# next time when we create a quiz we get the RAW results calculate them and save user data 


# a user can refresh modes only since his start date




def psedudo_get_quiz(user_data:UserData):
    # calculate_results from user_data
    user_data.calculate_results()
    # if mode is refresh we do not need to change the branch
    mode =  user_data.get_mode()
    parts = []
    if mode == 0:
        if user_data.should_change_main_branch():
            user_data.select_next_main_branch()
        elif user_data.should_change_branch():
            user_data.select_next_branch()
        parts = user_data.get_current_branch_parts()
    else:
        parts = user_data.get_refresh_parts()
    
    quiz = format_quiz(user_data.lang, user_data.to_lang, parts, mode)
    return quiz
