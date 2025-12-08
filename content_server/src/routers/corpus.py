from fastapi import APIRouter
from models.corpus import Corpus
from batch_tools.corpus import get_corpus

router = APIRouter()
 

@router.get("/")
async def get_corpus(request: Corpus):
    return await get_corpus(request)