from pydantic import BaseModel
from utils.db import get_pg_con, get_schema


async def get_quiz(lang, to_lang):
    conn = await get_pg_con()
    sql = f"""
    SELECT 
        lang.part_id as part_id,
        lang.lang as lang,
        lang.text as text,
        lang.recording as recording,
        lang.options as options,
        lang.words as words,
        to_lang.part_id as to_part_id,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.recording as to_recording,
        to_lang.options as to_options,
        to_lang.words as to_words
    from polyglots_quiz.parts as lang  
    join polyglots_quiz.parts as to_lang
    on lang.lang = '{lang}'
    AND to_lang.lang = '{to_lang}'
    AND lang.part_id = to_lang.part_id
    LIMIT 50
    """
    cursor =conn.cursor()
    res = await cursor.execute(sql)
    results = await cursor.fetchall()
    for rs in results:
        print(rs)