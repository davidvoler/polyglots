from fastapi import APIRouter
from models.translate import TranslateRequest

router = APIRouter()

@router.post("/")
async def translate(request: TranslateRequest):
    return {}    

@router.get("/review")
async def review_translation(request: TranslateRequest):
    return {}    

