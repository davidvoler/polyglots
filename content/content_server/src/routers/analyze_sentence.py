from fastapi import APIRouter
from models.analyze import AnalyzeRequest
from utils.batch_processing import set_batch_status
from batch_tools.analyze_sentence.analyzer import analyze_sentence_batch
import asyncio

router = APIRouter()

async def _analyze_sentences(request: AnalyzeRequest):
    set_batch_status(request, "start")
    await analyze_sentence_batch(request)
    set_batch_status(request, "done")

@router.post("/")
async def analyze_sentences(request: AnalyzeRequest):
    batch_id = set_batch_status(request, "create")
    asyncio.create_task(_analyze_sentences)
    return request
