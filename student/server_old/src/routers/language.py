from fastapi import APIRouter, Depends
from models.language import Language, DIALOGUE_LANGUAGES

router = APIRouter()

@router.get("/languages")
async def languages()->list[Language]:
   return DIALOGUE_LANGUAGES