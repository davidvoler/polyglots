from fastapi import APIRouter
from models.course import Course, CourseRequest
from utils.db import get_query_results, run_query

router = APIRouter()

@router.post("/", response_model=list[Course])
async def list_courses(request: CourseRequest):
    sql = """
    SELECT * FROM content_raw.courses WHERE lang = %s AND to_lang = %s
    """
    data = await get_query_results(sql, (request.lang, request.to_lang, request.limit, request.offset))
    return [Course(**row) for row in data]

async def create_course(request: CourseRequest):
    sql = """
    INSERT INTO content_raw.courses (lang, to_lang, name, description, created_by, school)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.lang, request.to_lang, request.name, request.description, request.created_by, request.school))
    return Course(id=id, lang=request.lang, to_lang=request.to_lang, name=request.name, description=request.description, created_by=request.created_by, school=request.school)

async def update_course(request: CourseRequest):
    sql = """
    UPDATE content_raw.courses SET name = %s, description = %s, created_by = %s, school = %s WHERE id = %s
    """
    await run_query(sql, (request.name, request.description, request.created_by, request.school, request.id))
    return Course(id=request.id, lang=request.lang, to_lang=request.to_lang, name=request.name, description=request.description, created_by=request.created_by, school=request.school)

async def delete_course(request: CourseRequest):
    sql = """
    DELETE FROM content_raw.courses WHERE id = %s
    """
    await run_query(sql, (request.id,))
    return Course(id=request.id, lang=request.lang, to_lang=request.to_lang, name=request.name, description=request.description, created_by=request.created_by, school=request.school)
