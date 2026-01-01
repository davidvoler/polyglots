from fastapi import APIRouter, Depends
from models.quiz import QuizRequest, Quiz
from utils.db import get_query_results
import time
router = APIRouter()
from utils.quiz_tatoeba.format import format_quiz
from models.modes import PracticeMode
from utils.lang_code import lang3_to_lang, lang_to_lang3
import random

@router.get("/get_lang_info")
async def lang_info(lang: str) -> dict:
    sql = """
    SELECT lang, count(*) as steps
    FROM tatoeba.steps
    WHERE lang = %s
    group by lang
    """
    data = await get_query_results(sql, (lang,))
    
    if not data:
        return {"error": "Language not found"}
    
    return {
        "lang": data[0]['lang'],
        "steps": data[0]['steps'],
    }
    
@router.get("/step")
async def get_step(lang: str, to_lang: str, step: int):
    t = time.time()
    sql = """
    SELECT * 
    FROM tatoeba.steps
    WHERE lang = %s
    AND to_lang = %s
    AND step>=%s
    AND step<=%s
    """
    data = await get_query_results(sql, (lang, to_lang, step,step+6))
    print(f"Getting step ids Query time: {time.time() - t} seconds")
    res = []
    # print(data)
    for r in data:
        res+=r.get('ids', [])
    return res
    

@router.post("/get_quiz")
async def get_quiz(quiz_req:QuizRequest)-> Quiz:
    lang = lang_to_lang3(quiz_req.lang)
    to_lang = lang_to_lang3(quiz_req.to_lang)
    try: 
        step = int(quiz_req.practice_id)
    except:
        step = random.randint(1, 500)
    ids = await get_step(lang, to_lang, step)
    
    ids = list(set(ids))
    random.shuffle(ids)
    ids = ids[:10]
    print(lang, to_lang, step, ids)
    
    placeholders = ', '.join(['%s'] * len(ids))
    t = time.time()
    sql =f"""SELECT 
        lang.part_id as part_id,
        lang.lang as lang,
        lang.text as text,
        lang.options as options,
        lang.words as words,
        lang.recording as recording,
        lang.translit as translit,
        lang.translit_details,
        to_lang.lang as to_lang,
        to_lang.text as to_text,
        to_lang.options as to_options,
        to_lang.words as to_words
    FROM tatoeba.links l
    JOIN  tatoeba.parts as lang  
    ON lang.part_id = l.id
    AND lang.lang = %s
    JOIN tatoeba.parts as to_lang
    ON to_lang.part_id = l.to_id
    AND to_lang.lang = %s
    WHERE l.lang = %s
    AND l.to_lang = %s
    AND l.id in ({placeholders})
    """
    #AND lang.recording != ''
    params = [lang, to_lang, lang, to_lang] + ids
    res = []
    data =  await  get_query_results(sql, params)
    print(f"Query time: {time.time() - t} seconds")
    for d in data:
        res.append(d)
    # print(res)
    quiz =  format_quiz(lang, to_lang, res, PracticeMode.step, reverse_mode=False)
    return quiz

async def get_step_particle(step):
        sql = """
        SELECT * 
        FROM tatoeba.particles
        WHERE level = %s
        """
        data = await get_query_results(sql, (step,))
        random.shuffle(data)
        return data[0]


@router.post("/get_particle_quiz")
async def get_particle_quiz(quiz_req:QuizRequest)-> Quiz:
    lang = lang_to_lang3(quiz_req.lang)
    to_lang = lang_to_lang3(quiz_req.to_lang)
    try: 
        step = int(quiz_req.practice_id)
    except:
        step = random.randint(1, 1000)
    # step = 1
    print(lang, to_lang, step)
    p_data = await get_step_particle(step)
    particle = p_data.get('particle', '')
    sql =f"""SELECT 
        lg.part_id as part_id,
        lg.lang as lang,
        lg.text as text,
        lg.options as options,
        lg.words as words,
        lg.recording as recording,
        tg.part_id as to_part_id,
        tg.lang as to_lang,
        tg.text as to_text,
        tg.options as to_options,
        tg.words as to_words
    FROM  tatoeba.particle_parts lg
    join tatoeba.particle_links l 
    on l.id=lg.part_id
    join  tatoeba.particle_parts tg
    on l.to_id = tg.part_id
    and tg.lang=%s
    where lg.lang = %s
    and lg.particle = %s
    """

    params = [to_lang,lang, particle]
    print(sql, params)
    res = []
    data =  await  get_query_results(sql, params)
    for d in data:
        res.append(d)
    # print(res)
    long_descriptions = p_data.get('long_descriptions', '')

    explanation_quiz = {
        "lang":lang,
        "to_lang": to_lang,
        "text":long_descriptions,
        "to_options" :["1","2","3"],
        "to_text": "to",
        "words":[],
        "sound": "",
        "part_id": -1,
    }
    print(res)
    quiz =  format_quiz(lang, to_lang, [explanation_quiz]+res, PracticeMode.step, reverse_mode=False)
    
    return quiz