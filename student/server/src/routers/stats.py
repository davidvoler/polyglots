from fastapi import APIRouter
from models.stats import StatsRequest, Stats
from utils.db import get_query_results

router = APIRouter()


@router.post("/stats")
async def stats(req: StatsRequest):
    where = "user_id = %s AND lang = %s AND to_lang = %s"
    params: list = [req.user_id, req.lang, req.to_lang]
    if req.course_id > 0:
        where += " AND course_id = %s"
        params.append(req.course_id)

    sql = f"""
    SELECT
        COUNT(DISTINCT lesson_id) AS lessons,
        COUNT(DISTINCT exercise_id) AS exercises,
        COUNT(*) FILTER (WHERE correct) AS correct_count,
        COUNT(*) AS total_count
    FROM users_data.results
    WHERE {where}
    """
    rows = await get_query_results(sql, tuple(params))
    if rows:
        r = rows[0]
        return Stats(
            user_id=req.user_id,
            lang=req.lang,
            to_lang=req.to_lang,
            course_id=req.course_id,
            lessons=r.get("lessons", 0) or 0,
            exercises=r.get("exercises", 0) or 0,
            correct=r.get("correct_count", 0) or 0,
            total=r.get("total_count", 0) or 0,
        )
    return Stats(user_id=req.user_id, lang=req.lang, to_lang=req.to_lang, course_id=req.course_id)
