from pydantic import BaseModel

class ReviewRequest(BaseModel):
    operation: str
    source: str
    review: bool = True
    limit: int = 300 
    offset: int = 0
    lang: str