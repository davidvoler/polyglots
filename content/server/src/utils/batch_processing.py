"""This module will handle batch processing stages
"""
import uuid
from models.batch_request import BatchRequest
from utils.db import run_query


async def set_batch_status(request: BatchRequest, status: str):
    """This function will create a record for the batch"""
    if not request.batch_id:
        request.batch_id = str(uuid.uuid4())
    sql = """
    insert into content_raw.batch_status(batch_id, operation, review, "limit", "offset", lang, action)
    values (%s, %s, %s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.batch_id, request.operation, request.review, 
                          request.limit, request.offset, request.lang, status))
    return request

async def delete_batch_data(request: BatchRequest):
    """When we are not happy with a batch we will delete the data"""
    sql = """
    insert into content_raw.batch_status(batch_id, operation, source, review, "limit", "offset", lang)
    values (%s, %s, %s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.batch_id, request.operation, request.source, request.review, request.limit, request.offset, request.lang))
    return request



"""
The stages for each batch processing are:
- run the process on a limited number of records 
- save to a temporary table
- review the results
- optional 
- accept and run on the entire corpus/language - now saving to the main table
- optional
- delete batch data
Question: Does a batch process overrides data from previous runs or save it to a batch table?
- options 1 - all batched are saved to a batch table - than copied to the main table 
- options 2 - save to main table override old batched
- options 3 - Decide per batch process
"""



