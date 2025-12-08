from utils.db import run_query
from models.review import ReviewRequest

def _get_translation_review_sql(lang: str, limit: int, offset: int):
    return """
    SELECT * FROM sentences
    WHERE lang = %s
    ORDER BY id DESC
    LIMIT %s
    OFFSET %s
    """

def _get_sentence_review_sql(lang: str, limit: int, offset: int):
    return """
    SELECT * FROM sentences
    WHERE lang = %s
    ORDER BY id DESC
    LIMIT %s
    OFFSET %s
    """

def _get_subtitles_review_sql(lang: str, limit: int, offset: int):
    return """
    SELECT * FROM subtitles
    WHERE lang = %s
    ORDER BY id DESC
    LIMIT %s
    OFFSET %s
    """

def _get_transliteration_review_sql(lang: str, limit: int, offset: int):
    return """
    SELECT * FROM transliteration
    WHERE lang = %s
    ORDER BY id DESC
    LIMIT %s
    OFFSET %s
    """

def _get_analysis_review_sql(lang: str, limit: int, offset: int):
    return """
    SELECT * FROM analysis
    WHERE lang = %s
    ORDER BY id DESC
    LIMIT %s
    OFFSET %s
    """

async def review_sentences(request: ReviewRequest):
    if request.operation == "translate":
        return await run_query(_get_translation_review_sql(request.lang, request.limit, request.offset))
    elif request.operation == "sentence":
        return await run_query(_get_sentence_review_sql(request.lang, request.limit, request.offset))
    elif request.operation == "subtitles":
        return await run_query(_get_subtitles_review_sql(request.lang, request.limit, request.offset))
    elif request.operation == "transliteration":
        return await run_query(_get_transliteration_review_sql(request.lang, request.limit, request.offset))
    elif request.operation == "analysis":
        return await run_query(_get_analysis_review_sql(request.lang, request.limit, request.offset))