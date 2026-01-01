from pydantic import BaseModel
from utils.scale import scale
from typing import Dict


class AppParam(BaseModel):
    name: str
    min_input: float
    max_inpurt: float
    min_output: float
    max_output: float
    steps: int = 20
    type: str = 'float' # int, float
    def get_value(self, avg_score: float):
        value = scale(avg_score, min_input=self.min_input, 
            max_input=self.max_input,
            min_output=self.min_output,
            max_output=self.max_output,
            scale_size=self.steps)
        if self.type == 'int':
            return int(round(value))
        return value


class AppParams(BaseModel):
    name: str
    params: Dict[str, AppParam] = {}
    def get_value(self, name: str, avg_score: float):
        ap = self.params.get(name)
        if ap:
            return ap.get_value(avg_score)
        return 0.0



APP_PARAMS_OPTIONS  = [
    AppParams(
        name = "A",
        params = {
            "branch_score": AppParam(
                name = "branch_score",
                min_input = -1.0,
                max_input = 1.0,
                min_output = 5.3,
                max_output = 1.7,
                steps = 20,
                type = "float"
            ),
            "referesh_score": AppParam(
                name = "referesh_avg_score",
                min_input = -1.0,
                max_input = 1.0,
                min_output = 6.0,
                max_output = 1.4,
                steps = 20,
                type = "float"
            ), 
            "referesh_factor": AppParam(
                name = "referesh_avg_score",
                min_input = -1.0,
                max_input = 1.0,
                min_output = 0.2,
                max_output = 0.015,
                steps = 20,
                type = "float"
            )

        }
    ),
    AppParams(
        name = "B",
        min_value = 0.0,
        max_value = 1.0,
        steps = 20,
        type = "float"
    )
]