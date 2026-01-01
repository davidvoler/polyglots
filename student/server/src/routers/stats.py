from fastapi import APIRouter, Depends
from models.stats import StatsRequest, Stats

router = APIRouter()

@router.post("/stats")
async def stats(req:StatsRequest):
   return Stats(
    user_id=req.user_id,
    lang=req.lang,
    to_lang=req.to_lang,
    course_id=req.course_id,
    lessons=0,
    exercises=0,
    words=0,
    sentences=0,
    alphabet=0
   )