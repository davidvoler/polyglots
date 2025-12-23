"""
len_elm is missing from from English
"""
from utils.db import run_query, get_query_results
import asyncio
from generators.course_template import CourseTemplate, create_course_template_with_words

LEN_C_GROUPS = [10, 15, 20,25,30,35,40,45]
LEN_C_GROUPS = [6, 15]
LEN_ELM_GROUPS = [(1,4), (4,6), (6,8), (8,10), (10,16)]


async def get_roots_by_len(from_ln:int, to_len:int):
    sql = """
    select root,root_lemma, count(*) as cnt from content_raw.sentence_elements 
    where lang='en' and len_elm <= %s and  len_elm <= %s and root=root_lemma and root !=''
    group by 1,2 order by 3 desc    
    """
    results = await get_query_results(sql, (from_ln, to_len))
    return results






async def gen_course(lang:str):
    for group in LEN_ELM_GROUPS:
        results = await get_roots_by_len(group[0], group[1])
        verbs = [(r.get('root'), r.get('cnt')) for r in results]
        j = 0
        for r in verbs[:100]:
            j+=1
            print(j,f". {r}")
        words = [v[0] for v in verbs[:200]]
        print(words[0:10])
        await create_course_template_with_words(CourseTemplate(), words)
