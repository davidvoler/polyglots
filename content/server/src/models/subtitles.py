from pydantic import BaseModel

class SubtitlesUploadRequest(BaseModel):
    corpus: str
    lang: str
    file_path: str
    file_type: str
    file_name: str
    media_source: str