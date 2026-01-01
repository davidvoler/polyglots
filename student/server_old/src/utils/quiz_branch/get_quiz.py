from models.quiz import QuizRequestBranch, Branch
from utils.db import get_query_results

async def should_switch_branch(req: QuizRequestBranch):
    pass

async def branch_word_selection(req: QuizRequestBranch) -> list[Branch]:
    sql = """
    SELECT * FROM tatoeba.branch2
    WHERE lang = %s
    AND max_wcount = %s
    """
    params = (req.lang, req.max_wcount)
    branches = []
    res = await get_query_results(sql, params)
    for r in res:
        branch = Branch(**r)
        branches.append(branch)
    return branches

async def get_quiz_branch(req: QuizRequestBranch):
    sql = """
    SELECT * FROM tatoeba.branch
    WHERE lang = %s
    AND key = %s
    AND max_wcount = %s
    AND level = %s
    """
    params = (req.lang, req.branch_key,  req.max_wcount, req.branch_key)
    res = await get_query_results(sql, params)
    return res

async def get_branchs(req: QuizRequestBranch):
    ''' return a list of branches  based on the same words with the same max_wcount'''
    pass

async def get_branch(lang: str, key: str):
    ''' return a list of branches  based on the same words with the same max_wcount'''
    sql = """
    SELECT * FROM tatoeba.branch
    WHERE lang = %s
    AND key = %s
    """
    params = (key,)
    braches = []
    res = await get_query_results(sql, params)
    for r in res:
        branch = Branch(**r)
        return branch
    return None

async def _get_quiz():
    sql = """
    SELECT * FROM tatoeba.links
    WHERE id in (%s)
    AND lang = %s
    AND to_lang = %s
    """
    params = (ids, lang, to_lang)
    res = await get_query_results(sql, params)
    return res