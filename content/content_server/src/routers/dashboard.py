from fastapi import APIRouter
from models.review import ReviewRequest
from utils.db import get_query_results

router = APIRouter()

async def load_dashboard_content():
    sql = """
    SELECT corpus, lang, count(*) as cnt FROM content_raw.sentences group by corpus, lang order by corpus, lang
    """
    data = await get_query_results(sql, None)
    return data
async def load_dashboard_content_elements():
    sql = """
    SELECT lang, count(*) as cnt FROM content_raw.sentence_elements group by lang order by lang
    """
    data = await get_query_results(sql, None)
    return data

async def load_dashboard_audio():
    sql = """
    SELECT audio_engine, lang, count(*) as cnt FROM content_raw.audio group by audio_engine, voice, lang order by audio_engine, voice, lang
    """
    data = await get_query_results(sql, None)
    return data




@router.get("/")
async def dashboard():
    sentences = await load_dashboard_content()
    sentence_elements = await load_dashboard_content_elements()
    audio = await load_dashboard_audio()
    return {
        "sentences": sentences,
        "sentence_elements": sentence_elements,
        "audio": audio
    }