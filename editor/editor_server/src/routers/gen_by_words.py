from fastapi import APIRouter
from models.gen_by_words import GenByWordsRequest
from utils.db import get_query_results, run_query

router = APIRouter()

@router.post("/", response_model=list[GenByWordsRequest])
async def gen_by_words(request: GenByWordsRequest):
    sql = """
    select root_lemma, count(*) from content_raw.sentence_elements 
    where lang = %d
    and len_elm <= %d
    group by 1 
    order by 2 desc
    """
    data = await get_query_results(sql, (request.course_id,))
    return [GenByWordsRequest(**row) for row in data]