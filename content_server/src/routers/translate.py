from fastapi import APIRouter
from models.batch_request import TranslateRequest
from batch_tools.translate import translate

router = APIRouter()
 

@router.post("/")
async def translate(request: TranslateRequest):
    return await translate(request)    


@router.get("/")
async def review_translation(request: TranslateRequest):
    return await translate(request)    


