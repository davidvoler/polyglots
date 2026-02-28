from fastapi import APIRouter
from utils.db import get_query_results

router = APIRouter()


@router.get("/lesson/{lesson_id}")
async def get_exercises_for_lesson(lesson_id: int):
    sql = """
    SELECT exercise_id, exercise_type, sentence, correct_options, wrong_options,
           audio_link, sentence_id, to_sentence_id
    FROM content.exercise
    WHERE lesson_id = %s
    ORDER BY exercise_id
    """
    rows = await get_query_results(sql, (lesson_id,))
    return rows
