from fastapi import APIRouter
from models.batch_request import TransliterateRequest
from batch_tools.transliterate import transliterate 

router = APIRouter()
 
@router.post("/")
async def transliterate(request: TransliterateRequest):
    return await transliterate(request) 

@router.get("/")
async def review_translation(request: TransliterateRequest):
    return await transliterate(request)    
