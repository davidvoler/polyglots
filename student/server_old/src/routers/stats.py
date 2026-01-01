from fastapi import APIRouter, Depends
from models.stats import StatsRequest, Stats
from utils.stats import single_query_stats, get_progress
router = APIRouter()

@router.post("/stats")
async def stats(req:StatsRequest):
   print(req)    
   res=  await single_query_stats(req)
   print(res)
   return res



@router.post("/progress")
async def progress(req:StatsRequest):
   print(req)    
   res=  await get_progress(req)
   print(res)
   return res