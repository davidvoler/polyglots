from utils.db import get_pg_con, run_query, get_query_results
import datetime
import asyncio
from models.user_vocab import UserVocab
from models.stats import Stats,StatsRequest
from models.preview import Preview, PreviewType, PreviewRequest, UserStatusResponse

import time



async def get_tags(req: PreviewRequest)-> list:
    sql = f"""
            SELECT 
                lang.tag_id,
                lang.tag as lang_tag,
                to_lang.tag as to_lang_tag
            FROM {req.customer_id}_quiz.tags as lang
            JOIN {req.customer_id}_quiz.tags as to_lang
            ON lang.lang = %s
            AND to_lang.lang = %s
            AND lang.tag_id = to_lang.tag_id
            ORDER BY lang.tag ASC
            LIMIT 10;
    """
    res =  await get_query_results(sql, (req.lang, req.to_lang),)
    results = []
    for r in res:
        results.append(Preview(
                    preview_id= r.get("tag_id"),
                    preview_type = PreviewType.tag,
                    header = r.get("to_lang_tag"),
                    words = [],
                    parts = [],
                    ul_words = [],
                    ul_parts = [],
                    new=0,
                    in_progress= 0,
                    done= 0,
                    completed = False
                ))
    return results

async def get_steps(req: PreviewRequest)-> list:
    sql = f"""
            SELECT 
                lang.step_id,
                lang.step,
                lang.words as lang_words,
                to_lang.words as to_lang_words
            FROM {req.customer_id}_quiz.steps as lang
            JOIN {req.customer_id}_quiz.steps as to_lang
            ON lang.lang = %s
            AND to_lang.lang = %s
            AND lang.step_id = to_lang.step_id
            ORDER BY lang.step ASC;
    """
    res =  await get_query_results(sql, (req.lang, req.to_lang),)
    results = []
    for r in res:
        results.append(
            Preview(
                    preview_id= r.get("step_id"),
                    preview_type = PreviewType.step,
                    header = "Step " + r.get("step_id"),
                    words = r.get("lang_words", []),
                    parts = [],
                    ul_words = r.get("to_lang_words", []),
                    ul_parts = [],
                    new=0,
                    in_progress= 0,
                    done= 0,
                    completed = False
                )
        )
    return results

async def get_dialogues(req: PreviewRequest)-> list:
    sql = f"""
            SELECT 
                lang.dialogue_id,
                lang.tag as lang_tag,
                to_lang.tag as to_lang_tag,
                lang.words as lang_words,
                to_lang.words as to_lang_words
            FROM {req.customer_id}_quiz.dialogue as lang
            JOIN {req.customer_id}_quiz.dialogue as to_lang
            ON lang.lang = %s
            AND to_lang.lang = %s
            AND lang.dialogue_id = to_lang.dialogue_id
            ORDER BY lang.step ASC
            LIMIT 10;
    """
    res =  await get_query_results(sql, (req.lang, req.to_lang),)
    results = []
    for r in res:
        results.append(Preview(
                    preview_id= r.get("dialogue_id"),
                    preview_type = PreviewType.dialogue,
                    header = r.get("lang_tag"),
                    words = r.get("lang_words", []),
                    parts = [],
                    ul_words = r.get("to_lang_words", []),
                    ul_parts = [],
                    new=0,
                    in_progress= 0,
                    done= 0,
                    completed = False
                ))
    return results



async def get_mixed(req:PreviewRequest)-> list:
    
    
    steps = await get_steps(req)
    tags = await get_tags(req)
    dialogues = await get_dialogues(req)
    mixed = steps + tags + dialogues
    return mixed


