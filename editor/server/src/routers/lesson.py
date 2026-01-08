from fastapi import APIRouter
from models.lesson import Lesson, LessonRequest
from utils.db import get_query_results, run_query

router = APIRouter()

@router.post("/", response_model=list[Lesson])
async def list_lessons(request: LessonRequest):
    sql = """
    SELECT * FROM content_raw.lessons WHERE course_id = %s
    """
    data = await get_query_results(sql, (request.course_id, request.limit, request.offset))
    return [Lesson(**row) for row in data]

async def create_lesson(request: LessonRequest):
    sql = """
    INSERT INTO content_raw.lessons (course_id, name, description, created_by, school)
    VALUES (%s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.course_id, request.name, request.description, request.created_by, request.school))
    return Lesson(id=id, course_id=request.course_id, name=request.name, description=request.description, created_by=request.created_by, school=request.school)

async def update_lesson(request: LessonRequest):
    sql = """
    UPDATE content_raw.lessons SET name = %s, description = %s, created_by = %s, school = %s WHERE id = %s
    """
    await run_query(sql, (request.name, request.description, request.created_by, request.school, request.id))
    return Lesson(id=request.id, course_id=request.course_id, name=request.name, description=request.description, created_by=request.created_by, school=request.school)

async def delete_lesson(request: LessonRequest):
    sql = """
    DELETE FROM content_raw.lessons WHERE id = %s
    """
    await run_query(sql, (request.id,))
    return Lesson(id=request.id, course_id=request.course_id, name=request.name, description=request.description, created_by=request.created_by, school=request.school)

async def generate_lesson(request: GenerateLessonRequest):
    sql = """
    INSERT INTO content_raw.lessons (course_id, name, description, created_by, school)
    VALUES (%s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.course_id, request.name, request.description, request.created_by, request.school))
    return Lesson(id=id, course_id=request.course_id, name=request.name, description=request.description, created_by=request.created_by, school=request.school)
    