from fastapi import APIRouter, Depends
from utils.db import get_query_results
router = APIRouter()


@router.get("/", response_model=list)
async def get_lang_info(lang: str) -> list:
    sql = f"""
    SELECT * FROM tatoeba.lang_info1 WHERE lang = %s
    """
    results = await get_query_results(sql, (lang,))
    res = []
    for row in results:
        res.append(row)
    return res
@router.get("/langs", response_model=dict)
async def get_langs_info(lang: str, to_lang:str) -> dict:
    sql = f"""
    SELECT * FROM tatoeba.lang_info1 WHERE lang = %s and to_lang = %s
    """
    results = await get_query_results(sql, (lang,to_lang,))
    res = []
    for row in results:
        return row
    
@router.get("/to_langs", response_model=list)
async def get_lang_info(lang: str) -> list:
    sql = f"""
    SELECT * FROM tatoeba.lang_info1 WHERE lang = %s
    """
    results = await get_query_results(sql, (lang,))
    res = []
    for row in results:
        res.append(row.get('to_lang'))
    return res
