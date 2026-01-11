from fastapi import APIRouter
from models.review import ReviewRequest
from utils.db import get_query_results
from models.dashboard import DashboardResponse, DashboardContent, DashboardContentElements, DashboardAudio


router = APIRouter()

async def load_dashboard_content():
    sql = """
    SELECT corpus, lang, count(*) as cnt FROM content_raw.sentences group by corpus, lang order by corpus, lang
    """
    data = await get_query_results(sql, None)
    return [DashboardContent(**row) for row in data]
async def load_dashboard_content_elements():
    sql = """
    SELECT lang, count(*) as cnt FROM content_raw.sentence_elements group by lang order by lang
    """
    data = await get_query_results(sql, None)
    return [DashboardContentElements(**row) for row in data]

async def load_dashboard_audio():
    sql = """
    SELECT audio_engine, lang, count(*) as cnt FROM content_raw.audio group by audio_engine, voice, lang order by audio_engine, voice, lang
    """
    data = await get_query_results(sql, None)
    return [DashboardAudio(**row) for row in data]




@router.get("/", response_model=DashboardResponse)
async def dashboard():
    sentences = await load_dashboard_content()
    sentence_elements = await load_dashboard_content_elements()
    audio = await load_dashboard_audio()
    return DashboardResponse(content=sentences, content_elements=sentence_elements, audio=audio)