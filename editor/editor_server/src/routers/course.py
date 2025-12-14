from fastapi import APIRouter
from models.course import Course, CourseRequest
from utils.db import get_query_results

router = APIRouter()

@router.post("/", response_model=list[Course])
async def list_courses(request: CourseRequest):
    sql = """
    SELECT * FROM content_raw.courses WHERE lang = %s AND to_lang = %s
    """
    data = await get_query_results(sql, (request.lang, request.to_lang, request.limit, request.offset))
    return [Course(**row) for row in data]