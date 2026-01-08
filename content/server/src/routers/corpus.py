from fastapi import APIRouter
from models.corpus import FileUploadResponse

router = APIRouter()
 

@router.get("/")
async def get_corpus(request: FileUploadResponse):
    return {}