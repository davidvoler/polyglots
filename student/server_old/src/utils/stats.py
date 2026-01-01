from utils.db import get_pg_con, run_query, get_query_results
import datetime
import asyncio
from models.user_vocab import UserVocab
from models.stats import Stats,StatsRequest, StatsElement, StatsElementGraph, Progress
import time
from utils.scale import scale


def compose_stats_results(req:StatsRequest, results:list)-> list:
    res = []
    i = 0
    for r in results:
        date_interval = r.get("date_interval")
        ccnt = r.get("ccnt", 0)
        if ccnt is None:
            ccnt = 0
        ncnt = r.get("ncnt", 0) 
        if ncnt is None:
            ncnt = 0
        jcnt = r.get("jcnt", 0)
        if jcnt is None:
            jcnt = 0
        jmark = r.get("jmark", 0)
        if jmark is None:
            jmark = 0
        jtimes = r.get("jtimes", 0)
        if jtimes is None:
            jtimes = 0
        label = "No Label"
        if req.granularity in ['week', 'week_days']:
            if date_interval:
                label = date_interval.strftime("%A")
        elif req.granularity == 'day': 
            if date_interval:
                label = date_interval.strftime("%H")   
        elif req.granularity == 'month':
            if date_interval:
                if i == 0:
                    d = date_interval + datetime.timedelta(days=1)
                    label = d.strftime("%b-%d")
                else:
                    label = date_interval.strftime("%b-%d")
        elif req.granularity == 'year':
            if date_interval:
                label = date_interval.strftime("%b")
        if jtimes >0 and jmark > 0:
            accuracy = int(round(scale(jmark/jtimes, 0.2, 1.0, 0, 100),0))
        else:
            accuracy = 0
        
        
        res.append(
                StatsElement(
                    label = label,
                    accuracy = accuracy,
                    new_items = ncnt,
                    completed_items = ccnt,
                    questions = jcnt
                )
            )
        i += 1
    graph = StatsElementGraph()
    for r in res:
        graph.label.append(r.label)
        graph.accuracy.append(r.accuracy)
        graph.new_items.append(r.new_items)
        graph.completed_items.append(r.completed_items)
        graph.questions.append(r.questions)
    return graph

async def single_query_stats(req:StatsRequest)-> list:
    if req.granularity == 'day':
        date_unit = "hour"
        steps = 23
        start_date = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
    elif req.granularity == 'week':
        date_unit = "day"
        steps = 6
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    elif req.granularity == 'week_days':
        date_unit = "day"
        steps = 6
        n = datetime.datetime.now()
        start_date = (datetime.datetime.now() - datetime.timedelta(days=n.weekday())).strftime("%Y-%m-%d")
    elif req.granularity == 'month':
        date_unit = "week"
        steps = 4
        n = datetime.datetime.now()
        start_date = n.strftime("%Y-%m-01")
    elif req.granularity == 'year':
        date_unit = "month"
        steps = 11
        n = datetime.datetime.now()
        start_date = n.strftime("%Y-01-01")
    sql =f"""
        SELECT f.date_interval, completed.ccnt,new_items.ncnt,  journal.jcnt, journal.jmark, journal.jtimes FROM (
            SELECT DATE_TRUNC('{date_unit}', '{start_date}'::TIMESTAMP + (n || ' {date_unit}s')::INTERVAL) AS date_interval
            FROM generate_series(0, {steps}) AS n) as f
        LEFT JOIN (
            SELECT 
            date_trunc('{date_unit}s', last_time) AS date_interval,
            COUNT(*) AS ccnt
            FROM  {req.customer_id}_users.user_content
            WHERE last_time > '{start_date}'::TIMESTAMP 
            AND lang = %s
            AND user_id = %s
            GROUP BY date_interval) as completed
        ON f.date_interval = completed.date_interval
        LEFT JOIN (
            SELECT 
                date_trunc('{date_unit}s', ts) AS date_interval,
                COUNT(*) AS jcnt,
                SUM(mark) AS jmark, 
                SUM(times) AS jtimes
            FROM {req.customer_id}_users.journal
            WHERE ts > '{start_date}'::TIMESTAMP 
            AND lang = %s
            AND user_id = %s
            GROUP BY date_interval
        ) as journal
        ON f.date_interval = journal.date_interval
        LEFT JOIN (
            SELECT 
            date_trunc('{date_unit}s', first_time) AS date_interval,
            COUNT(*) AS ncnt
            FROM  {req.customer_id}_users.user_content
            WHERE first_time > '{start_date}'::TIMESTAMP 
            AND lang = %s
            AND user_id = %s
            GROUP BY date_interval) as new_items
        ON f.date_interval = new_items.date_interval
        ORDER BY f.date_interval
    """
    # print(sql, (req.lang,req.user_id, ))
    
    res = await get_query_results(sql, (req.lang,req.user_id,req.lang,req.user_id,req.lang,req.user_id,),)
    # print(res)
    return compose_stats_results(req, res)


async def get_journal_stats(req: StatsRequest)-> list:
    if req.granularity == 'day':
        fld = "day"
        cnt = 7
    elif req.granularity == 'week':
        fld = "week"
        cnt = 4
    elif req.granularity == 'month':
        fld = "month"
        cnt = 3
    elif req.granularity == 'hour':
        fld = "hour"
        cnt = 24
    elif req.granularity == 'year':
        fld = "year"
        cnt = 3
    else:
        fld = "day"
        cnt = 7
    sql = f"""
            SELECT 
                date_trunc('{fld}', ts) AS {fld},
                COUNT(*) AS count,
                SUM(mark) AS mark,
                SUM(times) AS times 
            FROM {req.customer_id}_users.journal
            WHERE ts >= CURRENT_DATE - INTERVAL '{cnt} {fld}s'
            AND lang = %s
            AND user_id = %s
            GROUP BY {fld}
            ORDER BY {fld} ASC;
    """
    return await get_query_results(sql, (req.lang,req.user_id, ),)

async def get_new_items_stats(req: StatsRequest)-> list:
    """ returns new items stats for the last 7 days
    """
    if req.granularity == 'day':
        fld = "day"
        cnt = 7
    elif req.granularity == 'week':
        fld = "week"
        cnt = 4
    elif req.granularity == 'month':
        fld = "month"
        cnt = 12
    elif req.granularity == 'hour':
        fld = "hour"
        cnt = 24
    elif req.granularity == 'year':
        fld = "year"
        cnt = 3
    else:
        fld = "day"
        cnt = 7
    sql = f"""
            SELECT 
                date_trunc('{fld}', first_time) AS {fld},
                COUNT(*) AS count,
                SUM(mark) AS mark,
                SUM(times) AS times 
            FROM {req.customer_id}_users.user_content
            WHERE first_time >= CURRENT_DATE - INTERVAL '{cnt} {fld}s'
            AND lang = %s
            AND user_id = %s
            GROUP BY {fld}
            ORDER BY {fld} ASC;
    """
    return await get_query_results(sql, (req.lang,req.user_id, ),)

async def get_completed_items_stats(req:StatsRequest)-> list:
    """ returns new items stats for the last 7 days
    """
    if req.granularity == 'day':
        fld = "day"
        cnt = 7
    elif req.granularity == 'week':
        fld = "week"
        cnt = 4
    elif req.granularity == 'month':
        fld = "month"
        cnt = 3
    elif req.granularity == 'hour':
        fld = "hour"
        cnt = 24
    elif req.granularity == 'year':
        fld = "year"
        cnt = 3
    else:
        fld = "day"
        cnt = 7
    sql = f"""
            SELECT 
                date_trunc('{fld}', last_time) AS {fld},
                COUNT(*) AS count,
                SUM(mark) AS mark,
                SUM(times) AS times 
            FROM {req.customer_id}_users.user_content
            WHERE last_time >= CURRENT_DATE - INTERVAL '{cnt} {fld}s'
            AND lang = %s
            AND user_id = %s
            AND mark > %s
            GROUP BY {fld}
            ORDER BY {fld} ASC;
    """
    print(sql, (req.lang,req.user_id,2.2 ))
    return await get_query_results(sql, (req.lang,req.user_id,1.8 ),)

async def get_mark(req:StatsRequest):
    sql = f"""
            SELECT 
                mark AS mark,
                times AS times 
            FROM {req.customer_id}_users.journal
            WHERE  lang = %s
            AND user_id = %s
            ORDER BY ts DESC
            LIMIT 20;
    """
    res =  await get_query_results(sql, (req.lang,req.user_id, ),)
    if len(res) == 0:
        return 3.4
    m = 0
    t = 0
    for item in res:
        m += item.get("mark",0)
        t += item.get("times",0)
    if t> 20:
        return m/t
    return 3.4

async def get_step_stats(user_id:str, lang:str,step:str, customer_id:str='polyglots'):
    sql = f"""
    SELECT 
        sum(mark) as mark,
        sum(times) as times,
        count(*) as cnt
    FROM
    {customer_id}_users.journal
    WHERE 
        user_id=%s
        AND lang=%s
        AND step=%s
    """
    
    res =  await get_query_results(sql, (user_id, lang, step ),)
    # print(sql , (user_id, lang, step ))
    return res

async def get_dialogue_stats(user_id:str, lang:str,dialogue_id:str, customer_id:str='polyglots'):
    sql = f"""
    SELECT 
        sum(mark) as mark,
        sum(times) as times,
        count(*) as cnt
    FROM
    {customer_id}_users.journal
    WHERE 
        user_id=%s
        AND lang=%s
        AND dialogue_id=%S
    """
    res =  await get_query_results(sql, (user_id, lang, dialogue_id ),)
    return res


async def get_stats(req:StatsRequest)-> list:
    return await get_journal_stats(req)


    

async def full_stats(req:StatsRequest)-> list:
    journal = await get_journal_stats(req)
    new_items = await get_new_items_stats(req)
    completed_items = await get_completed_items_stats(req)
    # mark = await get_mark(req)
    # print (journal, new_items, completed_items, mark)
    results = []
    
    
    stats = Stats(
        user_id = req.user_id,
        lang = req.lang,
        journal = journal ,
        new_items = new_items ,
        mastered_items = completed_items,
        # mark = mark,
    )
    return stats




async def _get_questions_count(req:StatsRequest)-> int:
    sql = f"""SELECT count(*) as questions
    FROM {req.customer_id}_users.journal
    WHERE user_id=%s
    AND lang=%s 
    AND ts >= CURRENT_DATE - INTERVAL '1 day'
    """
    res = await get_query_results(sql, (req.user_id, req.lang,))
    if len(res) == 0:
        return 0
    try:
        return int(res[0].get("questions", 0))
    except:
        return 0


async def _get_words_count(req:StatsRequest)-> int:
    sql = f"""SELECT count(*) as words
    FROM {req.customer_id}_users.user_words
    WHERE user_id=%s
    AND lang=%s 
    AND last_time >= CURRENT_DATE - INTERVAL '1 day'
    """
    res = await get_query_results(sql, (req.user_id, req.lang,))
    if len(res) == 0:
        return 0
    try:
        return int(res[0].get("words", 0))
    except:
        return 0

async def _get_sentence_count(req:StatsRequest)-> int:
    sql = f"""SELECT count(*) as sentences
    FROM {req.customer_id}_users.user_content
    WHERE user_id=%s
    AND lang=%s 
    AND last_time >= CURRENT_DATE - INTERVAL '1 day'
    """
    res = await get_query_results(sql, (req.user_id, req.lang,))
    if len(res) == 0:
        return 0
    try:
        return int(res[0].get("sentences", 0))
    except:
        return 0


async def get_progress(req:StatsRequest)-> Progress:
    questions = await _get_questions_count(req)
    words = await _get_words_count(req)
    sentences = await _get_sentence_count(req)
    return Progress(
        user_id=req.user_id,
        lang=req.lang,
        questions=questions,
        words=words,
        sentences=sentences
    )
    
