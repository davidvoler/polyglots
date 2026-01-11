from pydantic import BaseModel



class FileUploadResponse(BaseModel):
    filename: str
    size: int
    content_type: str
    corpus: str = ''
    lang: str = ''
    to_lang: str = ''