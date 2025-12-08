from fastapi import APIRouter
from models.load_csv import LoadCsvRequest
from batch_tools.load_csv import load_csv

router = APIRouter()
 

@router.post("/")
async def load_csv(request: LoadCsvRequest):
    return await load_csv(request)