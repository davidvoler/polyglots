from fastapi import APIRouter
from models.analyze import AnalyzeRequest

router = APIRouter()

async def _analyze_sentences(request: AnalyzeRequest):
    return {}
 
@router.post("/")
async def analyze_sentences(request: AnalyzeRequest):
    return await _analyze_sentences(request)

