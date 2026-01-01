from utils.db import get_pg_con
from models.user_vocab import UserVocab
from models.modes import PracticeMode 
from utils.db import get_query_results
import random



async def get_step(lang, to_lang, step_id):
    sql =  f"""
    SELECT * 
    FROM tatoeba.steps 
    WHERE lang = %s
    and to_lang = %s
    AND step_id = %s
    """
    return await get_query_results(sql, (lang, to_lang, step_id,))


async def get_step_elements(lang, to_lang, ids:list):
    placeholders = ', '.join(['%s'] * len(ids))
    sql =f"""SELECT 
        lang.part_id as part_id,
        lang.lang as lang,
        lang.text as text,
        lang.options as options,
        lang.words as words,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.options as to_options,
        to_lang.words as to_words
    FROM tatoeba.links4 
    JOIN  tatoeba.parts as lang  
    ON lang.part_id = l.id
    AND lang.lang = %s
    JOIN tatoeba.parts as to_lang
    ON to_lang.part_id = l.to_id
    AND to_lang.lang = %s
    WHERE l.lang = %s
    AND l.to_lang = %s
    AND l.id in (placeholders)  
    """
    params = [lang, to_lang, lang, to_lang] + ids
    return await  get_query_results(sql, params)
    
