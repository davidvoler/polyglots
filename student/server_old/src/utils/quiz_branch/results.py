from utils.db import get_pg_con, run_query
from models.results import ResultsBranch
import datetime
import time
import random


async def _save_journal(results:ResultsBranch):
    if results.attempts == 1:
        mark = 1.0
    elif results.attempts == 2:
        mark = -0.8
    else:
        mark = -1.0
    sql = f"""
    INSERT INTO tatoeba_users.journal1 
    (
      lang, 
      user_id, 
      ts, 
      branch_key, 
      branch_word, 
      wcount, 
      answer_delay_ms, 
      play_times, 
      attempts, 
      mark, 
      part_id,
      word1,
      word2,
      word3,

    )
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    #for now we do not update bu save a new value for each save
    # later we could save values per minute and update ts
    params = (
        results.lang, 
        results.user_id, 
        time.time(), 
        results.branch_key, 
        results.branch_word, 
        results.wcount, 
        results.answer_delay_ms, 
        results.play_times, 
        results.attempts, 
        mark, 
        
    )
    await run_query(sql, params)

async def save_results(results:ResultsBranch, test_mode=False):
    # save journal
    await _save_journal(results)
    