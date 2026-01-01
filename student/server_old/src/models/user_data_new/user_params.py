from pydantic import BaseModel

class UserParams(BaseModel):
    step_len: int = 25
    branch_score: float = 6.0
    branch_times: int = 200
    refresh_score: float = 0.7
    refresh_factor: float = 0.3

    def calculate_step(self):
        pass    
    def calculate_refresh(self):
        pass