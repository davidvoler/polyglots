from fastapi import APIRouter, HTTPException
from models.generate import (
    ByWordsRequest, 
    ByWordResponse, 
    WordCount,
    CourseTemplateRequest,
    GeneratedCourse
)
from generators.course_template import CourseTemplate
from generators.generate import gen_course
from utils.db import get_query_results, run_query

router = APIRouter()

@router.post("/common_words", response_model=ByWordResponse)
async def comon_words(request: ByWordsRequest):
    limit_size = ''
    if request.words_count > 0:
        limit_size = f' and len_elm <= {request.words_count}' 
    sql = f"""
        SELECT word, count(*) as cnt
        FROM content_raw.sentence_elements 
        CROSS JOIN LATERAL (
        VALUES (word1), (word2), (word3), (word4)
        ) AS t(word)
        WHERE word IS NOT null
        and lang = %s
        {limit_size}
        GROUP BY 1
        order by 2 desc
        limit %s
        offset %s
    """
    print(sql)
    data = await get_query_results(sql, (request.lang,request.limit,request.offset))
    return ByWordResponse(words=[WordCount(**row) for row in data], 
        lang=request.lang, 
        words_count=request.words_count, 
        word_type=request.word_type,
        limit=request.limit,
        offset=request.offset)
    
@router.post("/common_root", response_model=ByWordResponse)
async def comon_root(request: ByWordsRequest):
    limit_size = ''
    if request.words_count > 0:
        limit_size = f' and len_elm <= {request.words_count}' 
    sql = f"""
    select root_lemma as word, count(*) as cnt from content_raw.sentence_elements 
    where lang = %s
    {limit_size}
    group by 1 
    order by 2 desc
    limit %s
    offset %s
    """
    print(sql)
    data = await get_query_results(sql, (request.lang,request.limit,request.offset))
    return ByWordResponse(words=[WordCount(**row) for row in data], 
        lang=request.lang, words_count=request.words_count, 
        word_type=request.word_type, total_words=len(data))


@router.post("/common_elements", response_model=ByWordResponse)
async def comon_elements(request: ByWordsRequest):
    limit_size = ''
    select_word = 'verb1'
    if request.words_count > 0:
        limit_size = f' and len_elm <= {request.words_count}' 
    if request.word_type == 'verb':
        select_word = 'verb1'
    elif request.word_type == 'noun':
        select_word = 'noun1'
    elif request.word_type == 'adjective':
        select_word = 'adjective1'
    elif request.word_type == 'adverb':
        select_word = 'adverb1'
    elif request.word_type == 'auxiliary_verb':
        select_word = 'auxiliary_verb1'
    sql = f"""
    select {select_word} as word, count(*) as cnt from content_raw.sentence_elements 
    where lang = %s
    and {select_word} is not null
    and {select_word} !=''
    group by 1 
    order by 2 desc
    limit %s
    offset %s
    """
    print(sql)
    data = await get_query_results(sql, (request.lang,request.limit,request.offset))
    return ByWordResponse(words=[WordCount(**row) for row in data], 
        lang=request.lang, words_count=request.words_count, 
        word_type=request.word_type, total_words=len(data))


@router.post("/course", response_model=GeneratedCourse)
async def generate_course(request: CourseTemplateRequest):
    """
    Generate a complete course based on the course template configuration.
    
    Args:
        request: CourseTemplateRequest with course generation parameters
    
    Returns:
        GeneratedCourse object containing the complete course structure
    """
    try:
        # Convert request to CourseTemplate
        course_template = CourseTemplate(
            lang=request.lang,
            to_lang=request.to_lang,
            words_per_module_start=request.words_per_module_start,
            words_per_module_increase_factor=request.words_per_module_increase_factor,
            sentence_length_start=request.sentence_length_start,
            sentence_length_increase_factor=request.sentence_length_increase_factor,
            verbs=request.verbs,
            nouns=request.nouns,
            adjectives=request.adjectives,
            adverbs=request.adverbs,
            grammar_per_module=request.grammar_per_module,
            greeting_module=request.greeting_module,
            reading_module=request.reading_module,
            reading_exercises=request.reading_exercises,
            writing_exercises=request.writing_exercises
        )
        
        # Generate the course
        generated_course = await gen_course(course_template)
        
        return generated_course
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating course: {str(e)}")