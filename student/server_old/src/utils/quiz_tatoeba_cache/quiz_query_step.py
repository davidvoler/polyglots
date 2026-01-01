from utils.db import get_pg_con
from models.user_vocab import UserVocab
from models.modes import PracticeMode 
from utils.db import get_query_results
import random



def  _get_base_parts_select(lang, 
                            to_lang, 
                            ids:list,
                            customer_id:str = 'tatoeba'):
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
    FROM {customer_id}_quiz.links4 
    JOIN  {customer_id}_quiz.parts as lang  
    ON lang.part_id = l.id
    AND lang.lang = %s
    JOIN {customer_id}_quiz.parts as to_lang
    ON to_lang.part_id = l.to_id
    AND to_lang.lang = %s
    WHERE l.lang = %s
    AND l.to_lang = %s
    AND l.id in (placeholders)  
    """
    params = [lang, to_lang, lang, to_lang] + ids
    return sql, params


async def _get_by_ids(lang,
                     to_lang,
                     ids:list, 
                     customer_id:str = 'tatoeba'):
    sql, params = _get_base_parts_select(lang, to_lang, ids, customer_id=customer_id)
    data=  await get_query_results(sql, (lang, params))
    return data    



async def get_refresh(user_id:str, 
                      lang:str, 
                      to_lang:str,
                      min_mark_refresh:float=7.0, 
                      customer_id:str = 'tatoeba' ):
    sort_orders =[
            "u_parts.last_time ASC",
            "u_parts.last_time ASC , u_parts.mark ASC",
            "u_parts.last_time ASC , u_parts.mark DESC" ,
            "u_parts.last_time ASC , u_parts.times ASC" ,
            "u_parts.last_time ASC , u_parts.times DESC",
        ]

    order_by = random.choice(sort_orders)
    print(f"order_by: {order_by}")
    sql = f"""
    SELECT part_id
    FROM {customer_id}_users.user_content 
    WHERE u_parts.lang < %s
    AND u_parts.user_id = %s
    ORDER BY {order_by}
    LIMIT 40
    """
    params = (lang,  user_id, min_mark_refresh)
    
    data = await get_query_results(sql, params)
    if len(data) == 0:
        return []
    search_ids = [d['part_id'] for d in data]
    return await _get_by_ids(lang, 
                             to_lang, 
                             search_ids, 
                             customer_id=customer_id)

async def get_repeat(user_id:str, 
                     lang:str, 
                     to_lang:str,
                     min_mark_repeat:float=5.1, 
                     customer_id:str = 'tatoeba' ):
    sort_orders =[
            "u_parts.last_time DESC",
            "u_parts.last_time DESC , u_parts.mark",
            "u_parts.last_time DESC , u_parts.mark DESC" ,
            "u_parts.last_time DESC , u_parts.times",
            "u_parts.last_time DESC , u_parts.times DESC",
        ]

    order_by = random.choice(sort_orders)
    print(f"order_by: {order_by}")
    sql = f"""
    SELECT part_id
    FROM {customer_id}_users.user_content 
    WHERE u_parts.lang < %s
    AND u_parts.user_id = %s
    ORDER BY {order_by}
    LIMIT 40
    """
    params = (lang,  user_id, min_mark_repeat)
    
    data = await get_query_results(sql, params)
    if len(data) == 0:
        return []
    search_ids = [d['part_id'] for d in data]
    return await _get_by_ids(lang, 
                             to_lang, 
                             search_ids, 
                             customer_id=customer_id)

async def get_by_words(user_id:str, 
                     lang:str, 
                     to_lang:str,
                     min_mark_repeat:float=3.1, 
                     max_mark_repeat:float=6.1, 
                     customer_id:str = 'tatoeba' ):

    sql = f"""
    SELECT steps.step as step, steps.ids as ids from {customer_id}_users.user_words uw
    LEFT JOIN {customer_id}_quiz.steps steps
    ON steps.word = uv.word
    AND steps.lang = %s
    WHERE lang = %s
    AND user_id = %s
    AND mark < %s
    AND mark > %s
    limit 10
    """
    params = (lang, lang,  user_id, min_mark_repeat, max_mark_repeat)
    
    data = await get_query_results(sql, params)
    if len(data) == 0:
        return []
    search_ids = []
    for d in data:
        step_ids = d.get('ids', [])
        if isinstance(step_ids, list) and len(step_ids) > 0:
            search_ids.append(step_ids[:10])
    return await _get_by_ids(lang, 
                             to_lang, 
                             search_ids, 
                             customer_id=customer_id)



async def get_user_step_status(user_id:str, lang:str, step:str, customer_id:str = 'tatoeba'):
    sql = f"""
    SELECT 
        step,
        count(*) as cnt,
        sum(mark) as mark,
        sum(times) as times
    FROM {customer_id}_users.journal
    WHERE user_id = %s
    AND lang = %s
    AND step = %s
    group by step
    """
    return await get_query_results(sql, (user_id, lang, step))


