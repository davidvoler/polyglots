from utils.db import get_pg_con
from models.user_vocab import UserVocab
from models.modes import PracticeMode 
from utils.db import get_query_results
import random



def _get_base_parts_select(customer_id:str = 'polyglots'):
    return f"""SELECT 
        lang.part_id as part_id,
        lang.lang as lang,
        lang.text as text,
        lang.recording as recording,
        lang.options as options,
        lang.words as words,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.recording as to_recording,
        to_lang.options as to_options,
        to_lang.words as to_words
    FROM {customer_id}_quiz.parts as lang  
    JOIN {customer_id}_quiz.parts as to_lang
    ON lang.lang = %s
    AND to_lang.lang = %s
    AND lang.part_id = to_lang.part_id
    """
def _get_base_dialogue_select(customer_id:str = 'polyglots'):
    return f"""SELECT 
        lang.dialogue_id as dialogue_id,
        lang.dialogue_line as dialogue_line,
        lang.lang as lang,
        lang.text as text,
        lang.recording as recording,
        lang.options as options,
        lang.words as words,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.recording as to_recording,
        to_lang.options as to_options,
        to_lang.words as to_words
    FROM {customer_id}_quiz.dialogue_line as lang  
    JOIN {customer_id}_quiz.dialogue_line as to_lang
    ON lang.lang = %s
    AND to_lang.lang = %s
    AND lang.dialogue_line = to_lang.dialogue_line
    """



async def get_step(step, lang, customer_id:str = 'polyglots'):
    sql = f"""
    SELECT * 
    FROM {customer_id}_quiz.steps 
    WHERE lang = %s
    AND step_id = %s
    """
    data=  await get_query_results(sql, (lang, step,))
    res = {}
    for d in data:
        return d 
    

async def get_by_dialogue(lang:str,to_lang:str, dialogues:list, customer_id:str = 'polyglots'):
    # TODO:
    # OPTIONS 1: Get a random dialogue -- current
    # OPTIONS 2:hat has the lowest mark 2 queries 
    random.shuffle(dialogues)
    dialogue_id = dialogues[0]
    sql = f"""
    {_get_base_dialogue_select(customer_id=customer_id)}
    WHERE lang.dialogue_id = %s
    ORDER BY lang.line_no
    """
    return await get_query_results(sql, (lang,to_lang, dialogue_id,))


    
    

async def get_lines_by_ids(user_id:str, lang:str, to_lang:str, lines:list, min_mark_practice:float, customer_id:str = 'polyglots'):
    random.shuffle(lines)
    lines = lines[:30]
    dialogue_id = []
    dialogue_lines = []
    for line in lines:
        did_l = line.split("_")
        if len(did_l) == 2:
            dialogue_id.append(did_l[0])
            dialogue_lines.append(int(did_l[1]))
    placeholders = ', '.join(['%s'] * len(lines))
    sql = f"""
    {_get_base_dialogue_select(customer_id=customer_id)}

    LEFT JOIN {customer_id}_users.user_content as u_lines
    ON u_lines.lang = %s
    AND u_lines.user_id = %s
    AND u_lines.dialogue_line = lang.dialogue_line
    WHERE (u_lines.mark < %s or u_lines.mark is null)
    AND lang.dialogue_line IN ({placeholders})
    """
    params = tuple([lang, to_lang, lang, user_id, min_mark_practice]+lines)
    return await get_query_results(sql, params)

async def get_parts_by_ids(user_id:str, lang:str, to_lang:str, min_mark_practice:float, ids:list, customer_id:str = 'polyglots' ):
    random.shuffle(ids)
    ids = ids[:100]
    placeholders = ', '.join(['%s'] * len(ids))
    sql = f"""
    {_get_base_parts_select(customer_id=customer_id)}
    LEFT JOIN {customer_id}_users.user_content as u_parts
    ON u_parts.lang = %s
    AND u_parts.user_id = %s
    AND u_parts.part_id = lang.part_id
    WHERE ( u_parts.mark < %s or u_parts.mark is null)
    AND lang.part_id IN ({placeholders})
    -- ORDER BY u_parts.last_updated
    
    """
    params = tuple([lang, to_lang, lang, user_id, min_mark_practice] + ids)
    return await get_query_results(sql, params)


async def get_parts_by_user_words(user_id:str, lang:str, to_lang:str, min_mark_practice:float, customer_id:str = 'polyglots' ):
    sorting = random.choice(["u_words.last_time DESC", " u_words.last_time DESC,  u_words.mark"])
    sql = f"""
    {_get_base_parts_select(customer_id=customer_id)}
    JOIN {customer_id}_users.user_words as u_words
    ON u_words.lang = %s
    AND u_words.user_id = %s
    AND u_words.word = lang.text
    WHERE u_words.mark < %s 
    order by {sorting}
    LIMIT 15
    """
    # print(f"get_parts_by_user_words: {sql} ")
    params = tuple([lang, to_lang, lang, user_id, min_mark_practice])
    # print(f"get_parts_by_user_words: {sql}  {params} ")
    return await get_query_results(sql, params)

async def get_parts_by_words(user_id:str, lang:str, to_lang:str, min_mark_practice:float, ids:list, words:list, customer_id:str = 'polyglots' ):
    search_ids = []
    if len(words) >7:
        random.shuffle(words)
        search_ids = words[:15]
    else:
        #use shortest ids that also include words 
        search_ids = ids[:15]
    placeholders = ', '.join(['%s'] * len(search_ids))
    sql = f"""
    {_get_base_parts_select(customer_id=customer_id)}
    LEFT JOIN {customer_id}_users.user_content as u_parts
    ON u_parts.lang = %s
    AND u_parts.user_id = %s
    AND u_parts.part_id = lang.part_id
    WHERE ( u_parts.mark < %s or u_parts.mark is null)
    AND lang.part_id IN ({placeholders})
    -- ORDER BY u_parts.last_updated
    """
    params = tuple([lang, to_lang, lang, user_id, min_mark_practice] + search_ids)
    return await get_query_results(sql, params)




async def get_refresh(user_id:str, lang:str, to_lang:str, min_mark_refresh:float=3.3, customer_id:str = 'polyglots' ):
    sort_orders =[
            "u_parts.last_time DESC",
            "u_parts.last_time DESC , u_parts.mark",
            "u_parts.last_time DESC , u_parts.mark DESC" ,
            "u_parts.last_time DESC , u_parts.times",
            "u_parts.last_time DESC , u_parts.times DESC",
            # "u_parts.last_time",
            # "u_parts.mark DESC",
            # "u_parts.mark",
            # "u_parts.times DESC",
            # "u_parts.times",
            # "u_parts.mark DESC , u_parts.last_time DESC",
        ]

    order_by = random.choice(sort_orders)
    print(f"order_by: {order_by}")
    sql = f"""
    {_get_base_parts_select(customer_id=customer_id)}
    LEFT JOIN {customer_id}_users.user_content as u_parts
    ON u_parts.lang = %s
    AND u_parts.user_id = %s
    AND u_parts.part_id = lang.part_id
    WHERE u_parts.mark < %s
    ORDER BY {order_by}
    LIMIT 20
    """
    params = (lang, to_lang, lang, user_id, min_mark_refresh)
    return await get_query_results(sql, params)

async def get_user_step_status(user_id:str, lang:str, step:str, customer_id:str = 'polyglots'):
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


