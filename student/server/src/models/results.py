from pydantic import BaseModel



class Results(BaseModel):
    user_id:str
    lang:str = ''
    exercise_id: int = 0
    lesson_id: int = 0
    module_id: int = 0
    course_id: int = 0
    verb: str = ''
    verb_lemma: str = ''
    noun: str = ''
    adjective: str = ''
    auxiliary: str = ''
    letter: str = ''
    attempts:int = 0
    answer_delay_ms: int = 0
    play_times: int = 0


