from utils.db import get_query_results

async def gen_alphabet_quiz(lang: str, to_lang: str):
    sql = """
    select letter, words_count from content_raw.alphabet where lang=%s and ab_type='%'
    """
    results = await get_query_results(sql, (lang, to_lang))
    return results


