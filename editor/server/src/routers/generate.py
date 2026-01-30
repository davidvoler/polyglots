from fastapi import APIRouter, HTTPException
from models.generate import (
    ByWordsRequest,
    ByWordResponse,
    WordCount,
    CourseTemplateRequest,
    GeneratedCourse,
    CourseOptionsResponse,
    LanguageOption,
    QuestionTypeOption,
    SentencesForWordRequest,
    SentencesForWordResponse,
    SentenceForWordItem,
    CreateCourseFromEditorRequest,
)
from generators.course_template import CourseTemplate
from generators.generate import gen_course
from utils.db import get_query_results, run_query

router = APIRouter()

# --- Editor flow: course options (step 1) ---

LANGUAGES = [
    LanguageOption(code="en", name="English"),
    LanguageOption(code="ja", name="Japanese"),
    LanguageOption(code="es", name="Spanish"),
    LanguageOption(code="fr", name="French"),
    LanguageOption(code="de", name="German"),
    LanguageOption(code="ar", name="Arabic"),
    LanguageOption(code="he", name="Hebrew"),
    LanguageOption(code="zh", name="Chinese"),
    LanguageOption(code="ko", name="Korean"),
]

QUESTION_TYPES = [
    QuestionTypeOption(id="sentence_single_choice", name="Single choice", description="Pick the correct translation", applicable_to="sentence"),
    QuestionTypeOption(id="sentence_multiple_choice", name="Multiple choice", description="Select all correct options", applicable_to="sentence"),
    QuestionTypeOption(id="identify_words_in_speech", name="Identify words", description="Identify words in the sentence", applicable_to="sentence"),
    QuestionTypeOption(id="letter_in_words", name="Letter in words", description="Find the letter in words", applicable_to="alphabet"),
    QuestionTypeOption(id="memory_game", name="Memory game", description="Match pairs", applicable_to="alphabet"),
    QuestionTypeOption(id="type_question", name="Type a word", description="Type the word", applicable_to="sentence"),
    QuestionTypeOption(id="words_in_grid", name="Words in grid", description="Find words in a grid", applicable_to="sentence"),
    QuestionTypeOption(id="explanation", name="Explanation", description="Read explanation", applicable_to="sentence"),
]


@router.get("/course_options", response_model=CourseOptionsResponse)
async def get_course_options():
    """Step 1: Return available languages and question types for course creation."""
    return CourseOptionsResponse(languages=LANGUAGES, question_types=QUESTION_TYPES)


@router.get("/question_types", response_model=list)
async def get_question_types():
    """Return list of question types for the editor (step 3b)."""
    return [qt.model_dump() for qt in QUESTION_TYPES]


@router.post("/sentences_for_word", response_model=SentencesForWordResponse)
async def sentences_for_word(request: SentencesForWordRequest):
    """Step 3a: Return candidate sentences (with translation and options) for a word, ordered by length."""
    sql = """
    SELECT l.id AS id, l.lang AS lang, l.text AS sentence, t.text AS translation, t.id AS to_id,
           t.lang AS to_lang, l.len_elm AS len_elm
    FROM content_raw.sentence_elements l
    JOIN content_raw.translation_links tl ON l.lang = tl.lang AND l.id = tl.id
    JOIN content_raw.sentences t ON tl.to_lang = t.lang AND tl.to_id = t.id
    WHERE tl.lang = %s AND tl.to_lang = %s
      AND (l.root = %s OR l.word1 = %s OR l.word2 = %s OR l.word3 = %s)
    ORDER BY l.len_elm
    LIMIT %s
    """
    rows = await get_query_results(sql, (request.lang, request.to_lang, request.word, request.word, request.word, request.word, request.limit))
    sentence_items = []
    for r in rows:
        opts = r.get("options")
        opts = list(opts) if isinstance(opts, (list, tuple)) and opts else []
        sentence_items.append(SentenceForWordItem(
            id=r["id"],
            to_id=r.get("to_id", 0),
            sentence=r["sentence"] or "",
            translation=r["translation"] or "",
            options=opts,
            len_elm=r.get("len_elm", 0),
        ))
    return SentencesForWordResponse(word=request.word, lang=request.lang, to_lang=request.to_lang, sentences=sentence_items)

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


@router.post("/create_course_from_editor")
async def create_course_from_editor(request: CreateCourseFromEditorRequest):
    """Step 4: Create course from editor choices; group lessons into modules."""
    if not request.selected_words:
        raise HTTPException(status_code=400, detail="selected_words is required")
    # Insert course
    sql_course = """
    INSERT INTO course.course (lang, to_lang, title, description)
    VALUES (%s, %s, %s, %s) RETURNING id
    """
    rows = await get_query_results(sql_course, (request.lang, request.to_lang, request.title or "New course", request.description or ""))
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to create course")
    course_id = rows[0]["id"]
    n = request.lessons_per_module or 10
    words = request.selected_words
    module_id = None
    for i, word in enumerate(words):
        if i % n == 0:
            sql_mod = """
            INSERT INTO course.module (course_id, lang, to_lang, title, description)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """
            title = f"Module {i // n + 1}"
            mod_rows = await get_query_results(sql_mod, (course_id, request.lang, request.to_lang, title, title))
            if not mod_rows:
                raise HTTPException(status_code=500, detail="Failed to create module")
            module_id = mod_rows[0]["id"]
        sql_lesson = """
        INSERT INTO course.lesson (course_id, module_id, lang, to_lang, title, description)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """
        lesson_rows = await get_query_results(sql_lesson, (course_id, module_id, request.lang, request.to_lang, word, word))
        if not lesson_rows:
            raise HTTPException(status_code=500, detail="Failed to create lesson")
        lesson_id = lesson_rows[0]["id"]
        # TODO: create exercises (single_choice, identify_words when automate_lesson; else from sentences_per_word + enabled_question_types)
    return {"course_id": course_id, "lang": request.lang, "to_lang": request.to_lang, "title": request.title}


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