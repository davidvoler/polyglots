from utils.db import get_query_results, run_query
import json
from batch_tools.analyze_sentence.ar.catt import diacritize
import pyarabic.araby as araby




def tokenize(text):
    return araby.tokenize(text)




async def analyze_sentence_batch_toc(lang:str, limit:int=0, offset:int=0):
    if limit:
        limit_offset = f' limit {limit} offset {offset}'
    else:
        limit_offset = ''
    table = 'content_raw.sentence_elements_simple2'
    on_conflict = 'on conflict (lang, id) do nothing'
    sql = f""" select * from content_raw.sentence_elements_simple where lang = %s order by id {limit_offset} """
    results = await get_query_results(sql, (lang, ))
    for r in results:
        len_elm = len(r.get('elements', []))
        if len_elm > 0:
            continue
        _id = r.get('id')
        text = r.get('text')
        words = tokenize(text)
        elm = [{"pos": "UKN", "text": w} for w in words]
        word1, word2, word3, word4 = '', '', '', ''
        if len(words) > 0:
            word1 = words[0]
        if len(words) > 1:
            word2 = words[1]
        if len(words) > 2:
            word3 = words[2]
        if len(words) > 3:
            word4 = words[3]
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
                r.get("text_alt1") , r.get("text_alt2") , r.get("text_alt3") ,
                json.dumps(elm),
                len(text), len(elm),
                words, word1, word2, word3, word4, r.get('options')))