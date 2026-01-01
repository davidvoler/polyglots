from pydantic import BaseModel
import random 
from utils.scale import scale 


class AppParams(BaseModel):
    name: str
    switch_branch_times_range: range = (150, 15)
    switch_main_branch_score_range: range = (700, 75)
    referesh_times: range = (90, 6)
    referesh_times_factor: range = (10, 2)
    refresh_score_factor: range = (0.5, 0.2)
    score_range: range = (6.2, 2.0 )
    refresh_days_range: range =[(0,10), (2, 3),  (7, 2),  (14, 2),  (21, 1),  (30, 1),  (60, 1),  (90, 1),  (120, 1)]
    level_range: range = (0, 10)
    wcount_range: range = (4, 6 ,9, 12, 15)
    evaluate_times: int = 25
    def get_score(self, avg_score: float):
        return scale(avg_score, 
                    -1,
                    1,
                    self.score_range[0], 
                    self.score_range[1], 
                    scale_size=25)
    def get_refresh_score_factor(self, avg_score: float):
        return scale(avg_score, 
                    -1,
                    1,
                    self.refresh_score_factor[0], 
                    self.refresh_score_factor[1], 
                    scale_size=25)
    def get_max_time(self, avg_score: float):
        return scale(avg_score, 
                    -1,
                    1,
                    self.max_times_range[0], 
                    self.max_times_range[1], 
                    scale_size=25)
    
    def get_max_time_factor(self, avg_score: float):
        return scale(avg_score, 
                    -1,
                    1,
                    self.referesh_times_factor[0], 
                    self.referesh_times_factor[1], 
                    scale_size=25)

APP_PARAMS_OPTIONS = [
    AppParams(
      switch_branch_times_range = (150, 15),
        name = "A",
        switch_main_branch_score_range = (700, 75),
        refresh_score_factor = (0.5, 0.2),
        refresh_days_range =[(0,10),  (2, 2),  (7, 2),  (14, 2),  (21, 1),  (30, 1),  (60, 1),  (90, 1),  (120, 1)],
        level_range = (0, 10),
        wcount_range = (4, 6 ,9, 12, 15),
        evaluate_times = 25
    ),
    AppParams(
        name = "B",
        switch_branch_times_range = (200, 20),
        switch_main_branch_score_range = (1000, 60),
        refresh_score_factor = (0.6, 0.1),
        refresh_days_range = [(0,10), (2, 1),  (7, 1),  (14, 1),  (21, 1),  (30, 1),  (60, 1),  (90, 1),  (120, 1), (180, 1)],
        level_range = (0, 10),
        wcount_range = (4, 6 ,9, 12, 15),
        evaluate_times = 30
    ),
]

def get_app_params(name: str) -> AppParams:
    return random.choice(APP_PARAMS_OPTIONS)