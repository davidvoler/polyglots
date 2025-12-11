from pydantic import BaseModel

class GenerateRequest(BaseModel):
    corpus: str
    lang: str
    to_lang: str
    review: bool = True
    limit: int = -1
    offset: int = 0