from utils.db import get_pg_con, run_query
from models.results import Results
import datetime
import time
import random


async def _save_journal(results:Results, test_mode=False):
    if results.attempts == 1:
        mark = 1
    else:
        mark = 0
    times = 1
    if test_mode:
        ts = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 1200), seconds=random.randint(0, 1000))
    else:
        ts = datetime.datetime.now() 
    sql = f"""
    INSERT INTO alphabet.journal 
    (
      lang, 
      user_id, 
      ts, 
      step, 
      mark, 
      times
    )
    VALUES 
    (%s, %s, %s, %s, %s, %s)
    """
    params = (
        results.lang, results.user_id, 
        ts, results.step, 
        mark, 
        times
    )
    await run_query(sql, params)

async def save_results(results:Results, test_mode=False):
    await _save_journal(results, test_mode=test_mode)

