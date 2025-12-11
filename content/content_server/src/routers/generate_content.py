from fastapi import APIRouter
from models.generate import GenerateRequest

router = APIRouter()

@router.post("/")
async def generate_content(request: GenerateRequest):
    return {}
    