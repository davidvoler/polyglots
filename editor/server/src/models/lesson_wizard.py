from pydantic import BaseModel



class LessonWizardRequest(BaseModel):
    course_id: int = 0
    word: str = ''
    words_so_far: list[str] = []


class SentencesWizardRequest(BaseModel):
    course_id: int = 0
    word: str
    lang: str
    to_lang: str
    words_so_far: list[str] = []

class SentencesWizardResponse(BaseModel):
    sentence_id: int
    sentence: str
    translation_id: int
    translation: str
    options: list[str]
