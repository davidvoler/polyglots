"""This module will handle batch processing stages
"""
import uuid
from models.batch_request import BatchRequest
from database import run_query


async def set_batch_status(request: BatchRequest, status: str):
    """This function will create a record for the batch"""
    if not request.batch_id:
        request.batch_id = str(uuid.uuid4())
    sql = """
    insert into content_raw.batches(batch_id, operation, source, review, limit, offset, lang)
    values (%s, %s, %s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.batch_id, request.operation, request.source, request.review, request.limit, request.offset, request.lang))
    return request

async def delete_batch_data(request: BatchRequest):
    """When we are not happy with a batch we will delete the data"""
    sql = """
    insert into content_raw.batches(batch_id, operation, source, review, limit, offset, lang)
    values (%s, %s, %s, %s, %s, %s, %s)
    """
    await run_query(sql, (request.batch_id, request.operation, request.source, request.review, request.limit, request.offset, request.lang))
    return request






