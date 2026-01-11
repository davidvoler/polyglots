from pydantic import BaseModel

class DashboardContent(BaseModel):
    corpus: str = ''
    lang: str = ''
    cnt: int = 0

class DashboardContentElements(BaseModel):
    lang: str = ''
    cnt: int = 0

class DashboardAudio(BaseModel):
    audio_engine: str = ''
    voice: str = ''
    lang: str = ''
    cnt: int = 0

class DashboardResponse(BaseModel):
    content: list[DashboardContent] = []
    content_elements: list[DashboardContentElements] = []
    audio: list[DashboardAudio] = []