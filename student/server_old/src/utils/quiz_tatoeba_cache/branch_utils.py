from utils.db import get_query_results
from models.quiz import Branch
import random





def get_next_branch(lang:str, 
                    root_word:str, 
                    words:list=[], 
                    branch_word:str=None,
                    max_wcount:int=4, 
                    compleated_branches:list=[],
                    max_level:int=None,
                    ):
    where = ""
    params = [lang, max_wcount]
    if branch_word:
        where += f" AND word = %s "
        params.append(branch_word)
    if max_level:
        where += f" AND level <= %s "
        params.append(max_level)
    if compleated_branches:
        params.extend(compleated_branches)
        where += f" AND key not in ({','.join(['%s']*len(compleated_branches))}) "
    if words:
        params.extend(words)
        where += f" AND word in ({','.join(['%s']*len(words))}) "
    sql = f"""
    SELECT * FROM tatoeba.branch
    WHERE lang = %s
    AND max_wcount = %s
    {where}
    limit 200"""
    res = get_query_results(sql, params)
    branches = [ Branch(**r) for r in res ]
    random.shuffle(branches)
    return branches[0]
