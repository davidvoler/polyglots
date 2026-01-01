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
    INSERT INTO tatoeba_users.journal 
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
    #for now we do not update bu save a new value for each save
    # later we could save values per minute and update ts
    params = (
        results.lang, results.user_id, 
        ts, results.step, 
        mark, 
        times
    )
    await run_query(sql, params)

async def _save_content(results:Results, test_mode=False):
    if results.attempts == 1:
        mark = 1.2
    elif results.attempts == 2:
        mark = -0.8
    else:
        mark = -1.0
    if test_mode:
        ts = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 1200), seconds=random.randint(0, 1000))
    else:
        ts = datetime.datetime.now()
    fields=  ','.join(['user_id', 
                       'lang', 'part_id', 
                       'first_time', 'last_time', 'mark', 'times'])
    values = [results.user_id, 
              results.lang, results.part_id,  

              ts, ts, mark, 1, 
              # updates
              ts, mark, 1 
              ]
    sql = f"""
    INSERT INTO tatoeba_users.user_parts
    ({fields}) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (lang, user_id, part_id) DO UPDATE
    SET last_time = %s, mark = user_parts.mark + %s, times = user_parts.times + %s
    """
    params = tuple(values)
    print (ts, mark)
    await run_query(sql, params)



async def _save_words(results:Results, test_mode=False):
    if results.attempts == 1:
        mark = 0.9
    elif results.attempts == 2:
        mark = -0.5
    else:
        mark = -0.6
    
    for w in results.words:
        ts = datetime.datetime.now()
        fields=  ','.join(['user_id', 'lang', 'word', 'last_time', 'mark', 'times'])
        values = [results.user_id, results.lang, w, 
                ts, mark, 1, 
                # updates
                ts, mark, 1 
                ]
        sql = f"""
        INSERT INTO tatoeba_users.user_words
        ({fields}) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (lang, user_id, word) DO UPDATE
        SET last_time = %s, mark = user_words.mark + %s, times = user_words.times + %s
        """
        params = tuple(values)
        await run_query(sql, params)


async def save_results(results:Results, test_mode=False):
    # save journal
    await _save_journal(results, test_mode=test_mode)
    # save content
    await _save_content(results, test_mode=test_mode)
    if len(results.words) > 0:
        await _save_words(results, test_mode=test_mode)

