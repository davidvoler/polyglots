from fastapi import APIRouter
from models.subtitles import SubtitlesUploadRequest

router = APIRouter()

@router.post("/")
async def analyze_subtitles(request: SubtitlesUploadRequest):
    return {}
    
    