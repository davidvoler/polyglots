from fastapi import APIRouter
from models.batch_request import BatchRequest
from batch_tools.subtitles import analyze_subtitles

router = APIRouter()
 

@router.post("/")
async def analyze_subtitles(request: BatchRequest):
    return await analyze_subtitles(request)    


@router.get("/")
async def review_subtitles(request: BatchRequest):
    pass 