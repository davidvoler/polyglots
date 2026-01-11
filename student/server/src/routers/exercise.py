from fastapi import APIRouter, Depends
from utils.db import get_query_results
router = APIRouter()

@router.get("/")
async def get_exercise():
   sql = """
   SELECT * FROM content.exercise
   where exercise_id in (29,800,2281,2,1,3361)
   """
   res = await get_query_results(sql, None)
   return res