from models.user_vocab import UserVocab
from datetime import datetime, timedelta


async def get_interval_back(granularity):
    if granularity == 'day':
        fld = "day"
        cnt = 7
    elif granularity == 'week':
        fld = "week"
        cnt = 4
    elif granularity == 'month':
        fld = "month"
        cnt = 3
    elif granularity == 'hour':
        fld = "hour"
        cnt = 24
    elif granularity == 'year':
        fld = "year"
        cnt = 3
    else:
        fld = "day"
        cnt = 7
    return fld, cnt





async def new_parts(granularity)-> list:
    sql = f"""
            SELECT 
                date_trunc('{fld}', first_time) AS {fld},
                COUNT(*) AS count,
                SUM(mark) AS mark,
                SUM(times) AS times 
            FROM {req.customer_id}_users.content
            WHERE last >= CURRENT_DATE - INTERVAL '{cnt} {fld}s'
            AND lang = %s
            AND user_id = %s
            GROUP BY {fld}
            ORDER BY {fld} ASC;
    """
async def practiced_parts(granularity)-> list:
    sql = f"""
            SELECT 
                date_trunc('{fld}', last_time) AS {fld},
                COUNT(*) AS count,
                SUM(mark) AS mark,
                SUM(times) AS times 
            FROM {req.customer_id}_users.content
            WHERE last >= CURRENT_DATE - INTERVAL '{cnt} {fld}s'
            AND lang = %s
            AND user_id = %s
            GROUP BY {fld}
            ORDER BY {fld} ASC;
    """

async def new_step(granularity)-> list:
    sql = f"""
            SELECT 
                date_trunc('{fld}', last_time) AS {fld},
                COUNT(*) AS count,
                SUM(mark) AS mark,
                SUM(times) AS times 
            FROM {req.customer_id}_users.content
            WHERE last >= CURRENT_DATE - INTERVAL '{cnt} {fld}s'
            AND lang = %s
            AND user_id = %s
            GROUP BY {fld}
            ORDER BY {fld} ASC;
    """

async def calc_achievements(uv:UserVocab):
    """
    Calculate the achievements for the user.
    """