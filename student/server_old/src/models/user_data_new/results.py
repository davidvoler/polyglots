from pydantic import BaseModel


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
