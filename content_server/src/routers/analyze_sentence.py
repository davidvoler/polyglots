from fastapi import APIRouter
from models.batch_request import AnalyzeSentenceRequest
from batch_tools.transliterate import transliterate 

router = APIRouter()
 
@router.post("/")
async def analyze_sentence(request: AnalyzeSentenceRequest):
    return await transliterate(request) 

@router.get("/")
async def review_sentence(request: AnalyzeSentenceRequest):
    return await transliterate(request)    
