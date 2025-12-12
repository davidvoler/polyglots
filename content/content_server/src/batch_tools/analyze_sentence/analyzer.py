import importlib
import re
from sqlite3 import DataError
from utils.db import get_query_results, run_query
import json
from batch_tools.analyze_sentence.with_spacy.sentence import has_spacy_model
from models.analyze import AnalyzeRequest



def get_analyzer(lang:str):
    try:
        module = importlib.import_module(f'batch_tools.analyze_sentence.{lang}.sentence')
    except ImportError:
        if has_spacy_model(lang):
            module = importlib.import_module(f'batch_tools.analyze_sentence.with_spacy.sentence')
        else:
            module = importlib.import_module(f'batch_tools.analyze_sentence.default.sentence')
    return module



def analyze_sentence(lang:str, text:str, id:int) -> dict:
    m = get_analyzer(lang)
    data = m.analyze_sentence(text, id, lang)
    return data



async def analyze_sentence_with_translit(lang:str):
    sql = """ select * from content_raw.sentences where lang = %s"""
    results = await get_query_results(sql, (lang,))
    for r in results:
        text = r.get('text')
        _id = r.get('id')
        data = analyze_sentence(lang, text, _id)
        sql = """ INSERT INTO content_raw.sentence_elements 
        (lang, id, text, elements, adverb1, adverb2, verb1, verb2, auxiliary_verb1, auxiliary_verb2, 
        noun1, noun2, adjective1, adjective2, verb_count, noun_count, adjective_count, adverb_count,
        len_c, len_elm,lang_extra)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s ,%s ,%s)
        on conflict (lang, id) do nothing
        """
        await run_query(sql, (lang, id, text, json.dumps(data.get('elements')), data.get('adverb1'), data.get('adverb2'), data.get('verb1'), data.get('verb2'), 
        data.get('auxiliary_verb1'), data.get('auxiliary_verb2'), data.get('noun1'), data.get('noun2'), data.get('adjective1'), data.get('adjective2'), 
        data.get('verb_count'), data.get('noun_count'), data.get('adjective_count'), data.get('adverb_count'),
        data.get('len_c'), data.get('len_e'),json.dumps(data.get('lang_extra'))))


async def analyze_sentence_batch(request: AnalyzeRequest):
    if request.is_preview:
        limit_offset = f"limit {request.limit} offset {request.offset}"
        table = 'content_raw.sentence_elements_preview'
        on_conflict = 'on conflict (lang, id, batch_id) do nothing'
    else:
        limit_offset = ''
        table = 'content_raw.sentence_elements'
        on_conflict = 'on conflict (lang, id) do nothing'
    sql = f""" select * from content_raw.sentences where lang = %s {limit_offset}"""
    results = await get_query_results(sql, (request.lang,))
    for r in results:
        text = r.get('text')
        _id = r.get('id')
        data = analyze_sentence(request.lang, text, _id)
        sql = f""" INSERT INTO {table}
        (lang, id, text, elements, adverb1, adverb2, verb1, verb2, auxiliary_verb1, auxiliary_verb2, 
        noun1, noun2, adjective1, adjective2, verb_count, noun_count, adjective_count, adverb_count,
        len_c, len_elm,lang_extra, batch_id)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s ,%s ,%s, %s)
        {on_conflict}
        """
        await run_query(sql, (request.lang, _id, text, json.dumps(data.get('elements')), data.get('adverb1'), data.get('adverb2'), data.get('verb1'), data.get('verb2'), 
        data.get('auxiliary_verb1'), data.get('auxiliary_verb2'), data.get('noun1'), data.get('noun2'), data.get('adjective1'), data.get('adjective2'), 
        data.get('verb_count'), data.get('noun_count'), data.get('adjective_count'), data.get('adverb_count'),
        data.get('len_c'), data.get('len_e'),json.dumps(data.get('lang_extra')), request.batch_id))
