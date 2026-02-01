from fastapi import APIRouter
from utils.db import get_query_results, run_query
from models.lesson_wizard import LessonWizardRequest, SentencesWizardRequest
router = APIRouter()


@router.get("/sentences", response_model=list[Lesson])
async def get_sentences(req:SentencesWizardRequest):
    pass 


@router.post("/", response_model=list[Lesson])
async def gen_lesson(request: LessonWizardRequest):
    sql = """
    SELECT * FROM content_raw.lessons WHERE course_id = %s
    """
    data = await get_query_results(sql, (request.course_id, request.limit, request.offset))
    return [Lesson(**row) for row in data]
