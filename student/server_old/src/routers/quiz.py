from fastapi import APIRouter, Depends
from models.quiz import QuizRequest, Quiz
from utils.quiz.get_quiz import get_quiz
from utils.quiz_tatoeba.get_quiz import get_quiz as get_quiz_tatoeba
from utils.quiz_kanji.get_quiz import get_quiz as get_quiz_kanji
router = APIRouter()
from fastapi import HTTPException

@router.post("/get_quiz", response_model=Quiz)
async def r_get_quiz(req: QuizRequest) -> Quiz:
    print('----------------------------------------------')
    print(req)
    print('----------------------------------------------')
    if True:
        quiz =  await get_quiz_kanji(req)
    else:
        if not req: 
            raise HTTPException(status_code=400, detail="User vocab not found")
        if req.corpus == 'tatoeba':
            quiz =  await get_quiz_tatoeba(req)
        else:
            quiz =  await get_quiz(req)
        # print('----------------------------------------------')
        print(quiz.mode, quiz.practice_id)
        # print('----------------------------------------------')
    return quiz