from fastapi import APIRouter, Depends
from models.course import CourseRequest, Course, Lesson, Module
from fastapi import HTTPException
from utils.db import get_query_results
router = APIRouter()




@router.post("/", response_model=list[Course])
async def get_course(req: CourseRequest) -> List[Course]:
    sql = """
    SELECT * FROM course.course WHERE lang = %s AND to_lang = %s
    """
    data = await get_query_results(sql, (req.lang, req.to_lang))
    return [Course(**row) for row in data]

   

@router.get("/course/{course_id}", response_model=Course)
async def get_course(course_id: int) -> Course:
    sql = """
    SELECT * FROM course.course WHERE id=%s
    """
    data = await get_query_results(sql, (course_id,))
    return Course(**data[0])
        