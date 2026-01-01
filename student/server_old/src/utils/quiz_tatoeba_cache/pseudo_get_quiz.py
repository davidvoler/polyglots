from models.quiz import QuizRequest
from user_data import get_or_create_user_data, save_user_data
from models.user_data import UserData
from models.quiz import Quiz
import asyncio 
MIN_PART_COUNT = 6


def _get_quiz(quiz_req:QuizRequest, parts:list):
    return parts, None

async def update_user_data(selected_parts:list, user_data:UserData):
    user_data.last_quiz_parts = selected_parts
    save_user_data(user_data)


def get_quiz(quiz_req:QuizRequest):
    user_data = get_or_create_user_data(quiz_req.user_id, quiz_req.lang)
    parts = user_data.get_current_branch_parts()
    if len(parts) < MIN_PART_COUNT:
        user_data.select_next_branch()
    parts = user_data.get_current_branch_parts()
    selected_parts, quiz = _get_quiz(quiz_req, parts)
    asyncio.create_task(update_user_data(selected_parts, user_data))
    return quiz