from pydantic import BaseModel
from models.user_data_new.history import UserHistory
from models.user_data_new.user_params import UserParams
from models.user_data_new.app_params import AppParams
from models.user_data_new.results import Results
from typing import List

class UserData(BaseModel):
    user_id: str
    lang: str
    history: UserHistory = UserHistory()
    user_params: UserParams = UserParams()
    app_params: AppParams = AppParams()
    results: List[Results] = []

    def get_parts(self):
        pass

    def switch_branch(self):
        pass

    def switch_main_branch(self):
        pass

    def cacluate_results(self):
        pass

    def save_results(self):
        pass

    def get_stats(self):
        pass

    def evaluate_results(self, results: list[Results]):
        pass
