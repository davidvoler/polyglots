from pydantic import BaseModel


class ReviewRequest(BaseModel):
    lang: str
    to_lang: str = ''
    limit: int = 300
    offset: int = 0


class Sentence(BaseModel):
    text: str = ''
    id: int = 0
    options: list[str] = []
    to_id: int = 0
    to_text: str = ''
    to_options: list[str] = []
    reviewed: bool = False
    review_accepted: bool = False
    review_comment: str = ''


class ReviewResponse(BaseModel):
    sentences: list[Sentence] = []
    limit: int = 300
    offset: int = 0