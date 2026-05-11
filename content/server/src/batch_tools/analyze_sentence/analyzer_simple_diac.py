from utils.db import get_query_results, run_query
import json
from batch_tools.analyze_sentence.ar.catt import diacritize







async def res_exists(lang:str, id:int):
    sql = f""" select count(*) as cnt  from content_raw.sentence_elements_simple1 where lang = %s and id = %s"""
    results = await get_query_results(sql, (lang, id))
    print(f"res_exists results: {results}")
    try:
        cnt = results[0].get('cnt', 0)
        return cnt > 0
    except:
        return False

async def analyze_sentence_batch_diac(lang:str, limit:int=0, offset:int=0):
    if limit:
        limit_offset = f' limit {limit} offset {offset}'
    else:
        limit_offset = ''
    table = 'content_raw.sentence_elements_simple1'
    on_conflict = 'on conflict (lang, id) do nothing'
    sql = f""" select * from content_raw.sentence_elements_simple where lang = %s order by id {limit_offset} """
    results = await get_query_results(sql, (lang, ))
    for r in results:
        # res_existsing = await res_exists(lang, r.get('id'))
        # if res_existsing:
        #     continue
        _id = r.get('id')
        text = r.get('text')
        text_alt1 = diacritize([text],verbose=False )
        text_alt2 = diacritize([text],verbose=True )
        print(f"text: {text}, text_alt1: {text_alt1}, text_alt2: {text_alt2}")
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
                text_alt1[0] if text_alt1 else '', text_alt2[0] if text_alt2 else '', '',
                json.dumps(r.get('elements')),
                r.get('len_c'), len(r.get('elements')), 
                r.get('words'), r.get('word1'), r.get('word2'), r.get('word3'), r.get('word4'), r.get('options')))
