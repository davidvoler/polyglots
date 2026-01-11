from pydantic import BaseModel

class BatchRequest(BaseModel):
    batch_id: str = ''
    lang: str 
    to_lang: str
    operation: str = ''
    corpus: str =''
    review: bool = True
    limit: int = -1 
    offset: int = 0
    stage: str = ''
    is_preview: bool = False

class TranslateRequest(BatchRequest):
    operation: str = "translate"
    to_lang: str

class AnalyzeRequest(BatchRequest):
    operation: str = "analyze"

class TransliterateRequest(BatchRequest):
    operation: str = "transliterate"

