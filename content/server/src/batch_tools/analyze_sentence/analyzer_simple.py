import importlib
import re
from sqlite3 import DataError
from utils.db import get_query_results, run_query
import json
from batch_tools.analyze_sentence.with_spacy.sentence import has_spacy_model
from models.analyze import AnalyzeRequest
from batch_tools.analyze_sentence.rank_words import get_ranked_words


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


async def get_last_completed_batch(lang:str):
    sql = f""" select max(id) as mx  from content_raw.sentence_elements where lang = %s"""
    results = await get_query_results(sql, (lang,))
    print(f"results: {results}")
    try:
        mx = results[0].get('mx', 0)
        if not mx:
            return 0
        return mx
    except:
        return 0


async def res_exists(lang:str, id:int):
    sql = f""" select count(*) as cnt  from content_raw.sentence_elements_simple where lang = %s and id = %s"""
    results = await get_query_results(sql, (lang, id))
    print(f"res_exists results: {results}")
    try:
        cnt = results[0].get('cnt', 0)
        return cnt > 0
    except:
        return False

async def analyze_sentence_batch(lang:str, limit:int=1000, offset:int=0):
    if limit:
        limit_offset = f' limit {limit} offset {offset}'
    else:
        limit_offset = ''
    table = 'content_raw.sentence_elements_simple'
    on_conflict = 'on conflict (lang, id) do nothing'
    sql = f""" select * from content_raw.sentences where lang = %s order by id {limit_offset} """
    results = await get_query_results(sql, (lang, ))
    for r in results:
        res_existsing = await res_exists(lang, r.get('id'))
        if res_existsing:
            continue
        text = r.get('text')
        _id = r.get('id')
        options = r.get('options')
        data = analyze_sentence(lang, text, _id)
        words_in_sentences = [d.get('text') for d in data.get('elements')]
        ranked_words = get_ranked_words(words_in_sentences, lang, words_count=4)
        word1 = ''
        word2 = ''
        word3 = ''
        word4 = ''
        if len(ranked_words) > 0:
            word1 = ranked_words[0]
            if len(ranked_words)> 1:
                word2 = ranked_words[1]
                if len(ranked_words) > 2:
                    word3 = ranked_words[2]
                    if len(ranked_words) > 3:
                        word4 = ranked_words[3]
        sql = f""" INSERT INTO {table}
        (lang, 
        id, 
        text, 
        text_alt1, 
        text_alt2, 
        text_alt3, 
        elements, 
        len_c, 
        len_elm,
        words, 
        word1, 
        word2, 
        word3, 
        word4, 
        options)
        values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
        {on_conflict}
        """
        await run_query(sql, (lang, _id, text, 
                data.get('text_alt1', ''), data.get('text_alt2', ''), data.get('text_alt3', ''),
                json.dumps(data.get('elements')),
                len(text), len(data.get('elements')), 
                words_in_sentences, word1, word2, word3, word4, options))
