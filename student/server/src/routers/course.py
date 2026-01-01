from fastapi import APIRouter, Depends
from models.course import CourseRequest, Course, Lesson, Module
from fastapi import HTTPException
from utils.db import get_query_results


router = APIRouter()


async def get_course_data(course_id: int) -> Course:
    modules = []
    sql = """
    SELECT id as module_id,* FROM course.module WHERE course_id=%s limit 10
    """
    data = await get_query_results(sql, (course_id,))
    modules = [Module(**row) for row in data]
    sql = """
    SELECT id as lesson_id,* FROM course.lesson WHERE course_id=%s limit 100
    """
    data = await get_query_results(sql, (course_id,))
    lessons = [Lesson(**row) for row in data]
    for m in modules:
        for l in lessons:
            if l.module_id == m.module_id:
                m.lessons.append(l)
        m.lessons_count = len(m.lessons)
    return Course(
        course_id=course_id,
        modules=modules,
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