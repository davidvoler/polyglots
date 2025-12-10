from fastapi import APIRouter
from models.review import ReviewRequest

router = APIRouter()
 




@router.get("/")
async def review(request: ReviewRequest):
    return await r