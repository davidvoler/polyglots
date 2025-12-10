from fastapi import APIRouter
from models.batch_request import AnalyzeRequest

router = APIRouter()
 
@router.post("/")
async def analyze_sentence(request: AnalyzeRequest):
    return await transliterate(request) 

