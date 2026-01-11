from fastapi import APIRouter
from models.review import ReviewRequest, ReviewResponse, Sentence, ReviewSentencesRequest
from utils.db import get_query_results

router = APIRouter()





@router.post("/", response_model=ReviewResponse)
async def review(request: ReviewRequest):
    sql = """
    select lg_source.text as text, lg_source.id as id ,lg_target.text as to_text, lg_target.id as to_id  from content_raw.sentences lg_source
    join content_raw.translation_links l on lg_source.id = l.id and lg_source.lang = l.lang 
    join content_raw.sentences lg_target on l.to_id = lg_target.id and  l.to_lang = lg_target.lang
    where lg_source.lang = %s and lg_target.lang = %s
    order by lg_source.id
    limit %s
    offset %s
    """
    data = await get_query_results(sql, (request.lang, request.to_lang, request.limit, request.offset))
    return ReviewResponse(sentences=[Sentence(**row) for row in data])


@router.post("/sentences", response_model=ReviewResponse)
async def review_sentences(request: ReviewSentencesRequest):
    """
    Review sentences for a given language
    """
    sql = """
      select * from content_raw.sentences_full
      where lang = %s
    order by id
    limit %s
    offset %s
    """
    data = await get_query_results(sql, (request.lang, request.limit, request.offset))
    return ReviewResponse(sentences=[Sentence(**row) for row in data])