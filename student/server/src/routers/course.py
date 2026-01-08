from fastapi import APIRouter, Depends
from models.course import CourseRequest, Course, Lesson, Module
from fastapi import HTTPException
from utils.db import get_query_results

router = APIRouter()

async def get_course_data(course_id: int) -> Course:
    modules = []
    sql = """
    SELECT id as module_id,* FROM course.module WHERE course_id=%s
    """
    data = await get_query_results(sql, (course_id,))
    modules = [Module(**row) for row in data]
    modules_keys = {m.module_id: m for m in modules}
    sql = """
    SELECT id as lesson_id,* FROM course.lesson WHERE course_id=%s
    """
    data = await get_query_results(sql, (course_id,))
    lessons = [Lesson(**row) for row in data]
    for l in lessons:
        if l.module_id in modules_keys:
            modules_keys[l.module_id].lessons.append(l)
    return Course(
        course_id=course_id,
        modules=list(modules_keys.values()),
    )



@router.post("/", response_model=list[Course])
async def get_course(req: CourseRequest) -> list[Course]:
    sql = """
    SELECT id as course_id,* FROM course.course WHERE lang = %s AND to_lang = %s
    """
    data = await get_query_results(sql, (req.lang, req.to_lang))
    return [Course(**row) for row in data]
   

@router.get("/course/{course_id}", response_model=Course)
async def get_course(course_id: int) -> Course:
    return await get_course_data(course_id)