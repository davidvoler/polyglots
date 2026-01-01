from fastapi import APIRouter, Depends
from models.quiz import QuizRequest, Quiz, QuizType
from fastapi import HTTPException
router = APIRouter()


async def get_lesson_quiz(req: QuizRequest) -> Quiz:
    return Quiz(id=1, name="Lesson 1", description="Lesson 1 description")
async def get_refresh_module_quiz(req: QuizRequest) -> Quiz:
    return Quiz(id=2, name="Refresh Module 1", description="Refresh Module 1 description")
async def get_refresh_course_quiz(req: QuizRequest) -> Quiz:
    return Quiz(id=3, name="Refresh Course 1", description="Refresh Course 1 description")
async def get_refresh_all_quiz(req: QuizRequest) -> Quiz:
    return Quiz(id=4, name="Refresh All 1", description="Refresh All 1 description")

@router.post("/get_quiz", response_model=Quiz)
async def r_get_quiz(req: QuizRequest) -> Quiz:
    match req.quiz_type:
        case QuizType.lesson:
            return await get_lesson_quiz(req)
        case QuizType.refresh_module:
            return await get_refresh_module_quiz(req)
        case QuizType.refresh_course:
            return await get_refresh_course_quiz(req)
        case QuizType.refresh_all:
            return await get_refresh_all_quiz(req)
        case _:
            raise HTTPException(status_code=400, detail="Invalid quiz type")



    

        