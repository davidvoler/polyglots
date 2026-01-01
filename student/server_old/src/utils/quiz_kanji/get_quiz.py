from models.quiz import QuizRequest, Quiz
from utils.db import get_query_results
import time
from utils.quiz_kanji.format import format_quiz
from models.modes import PracticeMode
from utils.lang_code import lang3_to_lang, lang_to_lang3
import random

async def get_by_group(lang: str, to_lang: str, step: int):
    sql = """
    SELECT word, kanji
    FROM alphabet.groups
    WHERE group_id=%s
    order by sub_group_id
    limit 10
    """

    data = await get_query_results(sql, (step,))
    print(f"kanji: {data[0].get('kanji')}")
    return [d.get('word') for d in data]    

async def get_single_kanji(lang: str, to_lang: str, step: int):
    sql = """
    SELECT word
    FROM alphabet.groups
    WHERE sub_group_id=1
    and group_id > %s
    order by sub_group_id
    limit 30
    
    """
    data = await get_query_results(sql, (step,))
    res = [d.get('word') for d in data]
    return random.choices(res, k=10)   



async def get_single_kanji_by_radical(lang: str, to_lang: str, step: int):
    sql = """
    select radical, count(*) as  cnt from alphabet.groups
    where sub_group_id = 1
    group by 1
    having count(*) > 6
    order by 2 desc

    """
    data = await get_query_results(sql, None)
    radicals = [d.get('radical') for d in data]
    radical = random.choice(radicals)
    print(f"radical: {radical}")
    sql = """
    SELECT word
    FROM alphabet.groups
    WHERE radical = %s
    and sub_group_id = 1
    limit 40
    """
    data = await get_query_results(sql, (radical,))
    res = [d.get('word') for d in data] 
    random.shuffle(res)
    return res[:10]


async def should_change_step(user_id:str, lang:str, to_lang:str, step:int)-> bool:
    sql = """
    SELECT sum(times) as times, sum(mark) as mark, 
    FROM alphabet.steps
    WHERE user_id = %s
    AND lang = %s
    AND to_lang = %s
    AND step = %s
    """
    data = await get_query_results(sql, (user_id, lang, to_lang, step))
    if not data:
        return False
    times = data[0].get('times', 0)
    mark = data[0].get('mark', 0)
    if times > 30:
        return True
    if mark > 0.7:
        return True
    return False

async def get_quiz_kanji(quiz_req:QuizRequest)-> Quiz:
    # should_change = await should_change_step(quiz_req.user_id, 
    #         quiz_req.lang, quiz_req.to_lang, quiz_req.step)
    should_change = True
    if should_change:
        quiz_req.step = random.randint(1, 300)
    if quiz_req.step %4 == 0:
        print(f"get_by_group: {quiz_req.step}")
        words = await get_by_group(quiz_req.lang, quiz_req.to_lang, quiz_req.step)
    elif quiz_req.step %3 == 0:
        print(f"get_single_kanji: {quiz_req.step}")
        words = await get_single_kanji(quiz_req.lang, quiz_req.to_lang, quiz_req.step)
    else:
        print(f"get_single_kanji_by_radical: {quiz_req.step}")
        words = await get_single_kanji_by_radical(quiz_req.lang, quiz_req.to_lang, quiz_req.step)
        
    random.shuffle(words)
    words = words[:10]
    placeholders = ', '.join(['%s'] * len(words))
    sql =f"""SELECT 
        lang.part_id as part_id,
        lang.lang as lang,
        lang.text as text,
        lang.options as options,
        lang.words as words,
        lang.recording as recording,
        lang.translit1 as translit,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.options as to_options,
        to_lang.words as to_words
    FROM alphabet.parts1 as lang  
    JOIN alphabet.parts1 as to_lang  
    ON lang.part_id = to_lang.part_id
    AND lang.lang = %s
    AND to_lang.lang = %s
    AND lang.part_id in ({placeholders})
    """
    #AND lang.recording != ''
    params = [quiz_req.lang, quiz_req.to_lang] + words
    data =  await  get_query_results(sql, params)
    return format_quiz(quiz_req.lang, quiz_req.to_lang, data, PracticeMode.step, reverse_mode=False)



async def get_quiz_common_words(quiz_req:QuizRequest)-> Quiz:
    sql = """select * from alphabet.common_words_groups where  lang = %s and words_count > 5 and ab_type = %s 
    order by words_count desc 
    limit 50"""
    data = await get_query_results(sql, (quiz_req.lang,'kanji' ))
    data = random.choice(data)
    print(f"seleccted kanji: {data.get('letter')}")
    words = data.get('words')
    return words

async def get_quiz_words(quiz_req:QuizRequest)-> Quiz:

    freq = random.randint(1, 500)
    words = await get_quiz_common_words(quiz_req)
    print(f"words: {words}")

    placeholders = ', '.join(['%s'] * len(words))
    sql =f"""SELECT 
        lang.part_id as part_id,
        lang.lang as lang,
        lang.text as text,
        lang.options as options,
        lang.recording as recording,
        lang.translit1 as translit,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.options as to_options
    FROM alphabet.parts2 as lang  
    JOIN alphabet.parts2 as to_lang  
    ON lang.part_id = to_lang.part_id
    AND lang.lang = %s
    AND to_lang.lang = %s
    and lang.part_id in ({placeholders})
    limit 20
    """
    params = [quiz_req.lang, quiz_req.to_lang] + words
    data =  await  get_query_results(sql, params)
    return format_quiz(quiz_req.lang, quiz_req.to_lang, data, PracticeMode.step, reverse_mode=False)


async def get_quiz(quiz_req:QuizRequest)-> Quiz:
    rnd = random.randint(1, 30)
    if rnd > 20:
        return await get_quiz_words(quiz_req)
    else:
        return await get_quiz_kanji(quiz_req)