"""
len_elm is missing from from English
"""
from utils.db import run_query, get_query_results
import asyncio
from generators.course_template import CourseTemplate, create_course_template_with_words
from models.generate import WordWithType

LEN_C_GROUPS = [10, 15, 20,25,30,35,40,45]
LEN_C_GROUPS = [6, 15]
LEN_ELM_GROUPS = [(1,4), (4,6), (6,8), (8,10), (10,16)]


async def get_roots_by_len(lang: str, from_ln: int, to_len: int):
    sql = """
    select root,root_lemma, count(*) as cnt from content_raw.sentence_elements 
    where lang=%s and len_elm >= %s and len_elm <= %s and root=root_lemma and root !=''
    group by 1,2 order by 3 desc    
    """
    results = await get_query_results(sql, (lang, from_ln, to_len))
    return results


async def get_words_by_type(lang: str, from_ln: int, to_len: int, word_type: str = None):
    """
    Get words with their types from the database.
    
    Args:
        lang: Language code
        from_ln: Minimum sentence length
        to_len: Maximum sentence length
        word_type: Optional filter for word type (verb, noun, adjective, adverb, auxiliary_verb)
    
    Returns:
        List of WordWithType objects
    """
    words_with_types = []
    
    # Query for different word types
    word_types_to_query = {
        'verb': 'verb1',
        'noun': 'noun1',
        'adjective': 'adjective1',
        'adverb': 'adverb1',
        'auxiliary_verb': 'auxiliary_verb1'
    }
    
    # If a specific type is requested, only query that type
    if word_type and word_type in word_types_to_query:
        types_to_query = {word_type: word_types_to_query[word_type]}
    else:
        types_to_query = word_types_to_query
    
    for wtype, column in types_to_query.items():
        sql = f"""
        select {column} as word, count(*) as cnt 
        from content_raw.sentence_elements 
        where lang=%s and len_elm >= %s and len_elm <= %s 
        and {column} is not null and {column} != ''
        group by {column} 
        order by cnt desc
        """
        results = await get_query_results(sql, (lang, from_ln, to_len))
        for r in results:
            word = r.get('word')
            if word:
                words_with_types.append(WordWithType(
                    word=word,
                    word_type=wtype,
                    count=r.get('cnt', 0)
                ))
    
    # Sort by count descending
    words_with_types.sort(key=lambda x: x.count or 0, reverse=True)
    return words_with_types






async def gen_course(course_template: CourseTemplate):
    """
    Generate a course based on course template configuration.
    
    Args:
        course_template: CourseTemplate instance with configuration parameters including lang and to_lang
    
    Returns:
        GeneratedCourse object with the complete course structure
    """
    from models.generate import GeneratedCourse
    from generators.course_template import gen_greeting_module
    
    # Generate greeting module if enabled
    greeting_module = None
    if course_template.greeting_module:
        greeting_module = await gen_greeting_module(course_template)
    
    all_modules = []
    
    for group in LEN_ELM_GROUPS:
        # Get words with types based on course template ratios
        all_words = await get_words_by_type(
            course_template.lang, 
            group[0], 
            group[1]
        )
        
        # Filter and select words based on template ratios
        selected_words = []
        
        # Calculate how many of each type based on ratios
        total_needed = 200  # Total words to select
        verb_count = int(total_needed * course_template.verbs)
        noun_count = int(total_needed * course_template.nouns)
        adjective_count = int(total_needed * course_template.adjectives)
        adverb_count = int(total_needed * course_template.adverbs)
        
        # Select words by type
        verbs = [w for w in all_words if w.word_type == 'verb'][:verb_count]
        nouns = [w for w in all_words if w.word_type == 'noun'][:noun_count]
        adjectives = [w for w in all_words if w.word_type == 'adjective'][:adjective_count]
        adverbs = [w for w in all_words if w.word_type == 'adverb'][:adverb_count]
        
        selected_words = verbs + nouns + adjectives + adverbs
        
        # Sort by count (most common first)
        selected_words.sort(key=lambda x: x.count or 0, reverse=True)
        
        # Generate modules from selected words
        modules = await create_course_template_with_words(course_template, selected_words)
        all_modules.extend(modules)
    
    return GeneratedCourse(
        lang=course_template.lang,
        to_lang=course_template.to_lang,
        greeting_module=greeting_module,
        modules=all_modules
    )
