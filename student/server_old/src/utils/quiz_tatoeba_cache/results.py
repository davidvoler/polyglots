from utils.db import get_pg_con, run_query, get_aerospike_client
from aerospike_helpers.operations import map_operations, operations
import aerospike
from models.results import Results
import datetime
import time
import random



def _save_journal(results:Results, test_mode=False):
    client = get_aerospike_client()
    as_key = ('tatoeba_users', 'journal', f'{results.user_id}:{results.lang}:{time.time()}')
    dict_data = results.model_dump()
    client.put(as_key, dict_data)

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
    client = get_aerospike_client()
    map_policy = {
        'map_write_flags': aerospike.MAP_WRITE_FLAGS_CREATE_ONLY
    }
    as_key = ('tatoeba_users', 'user_data', f'{results.user_id}:{results.lang}')
    ops = [
        operations.write('user_id', results.user_id),
        operations.write('lang', results.lang),
        map_operations.map_increment('parts_mark',  results.part_id, mark),
        map_operations.map_increment('parts_times',  results.part_id, 1),
        map_operations.map_increment('parts_last',  results.part_id, ts),
        map_operations.map_increment('parts_first',  results.part_id, ts, map_policy),
    ]
    for word in results.words:
        ops.append(map_operations.map_increment('words_mark',  word, mark))
        ops.append(map_operations.map_increment('words_times',  word, 1))
        ops.append(map_operations.map_increment('words_last',  word, ts))
        ops.append(map_operations.map_increment('words_first',  word, ts, map_policy))
    #use only when in branch parctice mode
    if results.branch_key:
        operations.increment('current_branch_times', 1)
        operations.increment('current_branch_mark', mark)
        operations.increment('current_branch_last', ts)
    client.operate(as_key, ops)


async def save_results(results:Results, test_mode=False):
    # save journal
    await _save_journal(results, test_mode=test_mode)
    # save content
    await _save_content(results, test_mode=test_mode)
    
