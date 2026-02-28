from fastapi import APIRouter
from models.results import Results
from utils.db import run_query

router = APIRouter()


@router.post("/save_results")
async def r_save_results(results: Results):
    sql = """
    INSERT INTO users_data.results
        (user_id, lang, to_lang, course_id, module_id, lesson_id,
         exercise_id, exercise_type, correct, attempts, answer_delay_ms)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    await run_query(sql, (
        results.user_id, results.lang, results.to_lang,
        results.course_id, results.module_id, results.lesson_id,
        results.exercise_id, results.exercise_type, results.correct,
        results.attempts, results.answer_delay_ms,
    ))
    return {"status": "ok"}
