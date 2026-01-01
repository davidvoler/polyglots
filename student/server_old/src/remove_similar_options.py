from utils.db import get_query_results, run_query
from utils.content_gen.similarity import get_similarity_score_simple
import asyncio

async def get_similarity_options(data, id_name):
    res = {}
    for d in data:
        # print(d.get('text', ''))
        # print(d.get('options', []))
        sim = get_similarity_score_simple(d.get('text', ''), d.get('options', []))
        i = 0
        found  = []
        for o in sim:
            if o[1] >= 0.92:
                print(d.get('text', ''), '<->', o[0], o[1], i)
                found.append(i)
            i += 1
        if len(found) > 0:
            res[d.get(id_name, '')] = found
    return res


async def remove_options(table, id_name,   _id, remove_idx:list):
    sql = f"""
    select text, options, lang
    FROM polyglots_quiz.{table}
    WHERE  {id_name}= %s
    """
    data=await get_query_results(sql, (_id,))

    for d in data:
        options = d.get('options', [])
        new_options = []
        lang = d.get('lang', '')
        text = d.get('text', '')
        i = 0
        for o in options:
            if i not in remove_idx:
                new_options.append(o)
            else:
                print("remove", o, text)
            i += 1
        # print("new options", new_options)
        sql = f"""
        UPDATE polyglots_quiz.{table}
        SET options = %s
        WHERE {id_name} = %s
        AND lang = %s
        """
        # print(sql, (new_options, _id, lang))
        print(_id, lang)
        await run_query(sql, (new_options, _id, lang))


async def get_dialogue_lines():
    sql = f"""
    SELECT * 
    FROM polyglots_quiz.dialogue_line
    WHERE lang = 'en'

    """
    data=  await get_query_results(sql, ())
    res=await get_similarity_options(data, 'dialogue_line')
    for k, v in res.items():
        print(k, v)
        await remove_options('dialogue_line', 'dialogue_line', k, v)

    

async def get_parts():
    sql = f"""
    SELECT * 
    FROM polyglots_quiz.parts
    WHERE lang = 'en'
    """
    data= await get_query_results(sql, ())
    res = await get_similarity_options(data, 'part_id')
    # print(res)
    for k, v in res.items():
        print(k, v)
        await remove_options('parts', 'part_id', k, v)
asyncio.run(get_dialogue_lines())    
# asyncio.run(get_parts())    