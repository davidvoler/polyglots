from fastapi import APIRouter, Depends
from models.results import Results
router = APIRouter()



@router.post("/save_results")
async def r_save_results(results: Results):
   print(results)