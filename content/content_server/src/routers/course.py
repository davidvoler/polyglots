from fastapi import APIRouter
from models.course import Course, Lesson, Step, CourseRequest
from utils.db import get_query_results

router = APIRouter()

@router.post("/", response_model=list[Course])
async def review(request: CourseRequest):
    sql = """
    SELECT * FROM content_raw.courses WHERE lang = %s AND to_lang = %s
    """
    data = await get_query_results(sql, (request.lang, request.to_lang, request.limit, request.offset))
    return [Course for row in data]


@router.post("/lessons", response_model=list[Lesson])
async def review_sentences(course_id: int):
    """
    Review sentences for a given language
    """
    sql = """
      SELECT * FROM content_raw.lessons WHERE course_id = %s
    """
    data = await get_query_results(sql, (course_id,))
    return [Lesson(**row) for row in data]




@router.post("/generate_course", response_model=list[Lesson])
async def review_sentences(course_id: int):
    """
    Review sentences for a given language
    """
    sql = """
      SELECT * FROM content_raw.lessons WHERE course_id = %s
    """
    data = await get_query_results(sql, (course_id,))
    return [Lesson(**row) for row in data]



