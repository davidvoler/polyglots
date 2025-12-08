from pydantic import BaseModel

class BatchRequest(BaseModel):
    operation: str
    source: str
    review: bool = True
    limit: int = -1 
    offset: int = 0
    lang: str

class TranslateRequest(BatchRequest):
    operation: str = "translate"
    to_lang: str

class AnalyzeRequest(BatchRequest):
    operation: str = "analyze"

class TransliterateRequest(BatchRequest):
    operation: str = "transliterate"

