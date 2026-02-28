import json
import random
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
    SaveEditorDraftRequest,
    EditorDraftResponse,
    EditorDraftListItem,
    EditorDraftWord,
    GenerateQuestionsRequest,
    GenerateQuestionsResponse,
    GeneratedExercisePreview,
    SaveLessonRequest,
    SaveLessonResponse,
    ModuleExercisesRequest,
    ModuleExercisesResponse,
    WordExercisesResult,
    CourseDetail,
    ModuleDetail,
    LessonDetail,
    ExerciseDetail,
    DeleteExercisesRequest,
)
from generators.course_template import CourseTemplate
from generators.generate import gen_course
from utils.db import get_query_results, run_query

router = APIRouter()


async def _get_audio_link(lang: str, sentence_id: int) -> str:
    sql = "SELECT recording FROM content_raw.audio WHERE lang = %s AND id = %s ORDER BY audio_engine LIMIT 1"
    rows = await get_query_results(sql, (lang, sentence_id))
    return rows[0].get('recording') if rows else ""


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
    """Step 3a: Return candidate sentences (with translation and options) for a word, ordered by sentence length (shortest first)."""
    sql = """
    SELECT l.id AS id, l.lang AS lang, l.text AS sentence, t.text AS translation, t.id AS to_id,
           t.lang AS to_lang, l.len_elm AS len_elm, t.options AS options
    FROM content_raw.sentence_elements l
    JOIN content_raw.translation_links tl ON l.lang = tl.lang AND l.id = tl.id
    JOIN content_raw.sentences t ON tl.to_lang = t.lang AND tl.to_id = t.id
    WHERE tl.lang = %s AND tl.to_lang = %s
      AND (l.root = %s OR l.word1 = %s OR l.word2 = %s OR l.word3 = %s)
    ORDER BY l.len_elm ASC NULLS LAST
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
    INSERT INTO content.course (lang, to_lang, title, description)
    VALUES (%s, %s, %s, %s) RETURNING id
    """
    rows = await get_query_results(sql_course, (request.lang, request.to_lang, request.title or "New course", request.description or ""))
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to create course")
    course_id = rows[0]["course_id"]
    n = request.lessons_per_module or 10
    words = request.selected_words
    module_id = None
    for i, word in enumerate(words):
        if i % n == 0:
            sql_mod = """
            INSERT INTO content.module (course_id, lang, to_lang, title, description)
            VALUES (%s, %s, %s, %s, %s) RETURNING module_id
            """
            title = f"Module {i // n + 1}"
            mod_rows = await get_query_results(sql_mod, (course_id, request.lang, request.to_lang, title, title))
            if not mod_rows:
                raise HTTPException(status_code=500, detail="Failed to create module")
            module_id = mod_rows[0]["module_id"]
        sql_lesson = """
        INSERT INTO content.lesson (course_id, module_id, lang, to_lang, title, description)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING lesson_id
        """
        lesson_rows = await get_query_results(sql_lesson, (course_id, module_id, request.lang, request.to_lang, word, word))
        if not lesson_rows:
            raise HTTPException(status_code=500, detail="Failed to create lesson")
        lesson_id = lesson_rows[0]["lesson_id"]
        # TODO: create exercises (single_choice, identify_words when automate_lesson; else from sentences_per_word + enabled_question_types)
    return {"course_id": course_id, "lang": request.lang, "to_lang": request.to_lang, "title": request.title}


# --- Editor draft: save / list / get / update ---

def _draft_from_row(r) -> EditorDraftResponse:
    words = r.get("words_with_weight") or []
    if isinstance(words, str):
        words = json.loads(words) if words else []
    spw = r.get("sentences_per_word") or {}
    if isinstance(spw, str):
        spw = json.loads(spw) if spw else {}
    return EditorDraftResponse(
        id=r["id"],
        created_at=str(r.get("created_at", "")),
        updated_at=str(r.get("updated_at", "")),
        title=r.get("title") or "",
        description=r.get("description") or "",
        lang=r["lang"],
        to_lang=r["to_lang"],
        selected_question_type_ids=list(r.get("selected_question_type_ids") or []),
        words_with_weight=[EditorDraftWord(word=x["word"], weight=x.get("weight", 0)) for x in words],
        step=int(r.get("step", 0)),
        automate_lesson=bool(r.get("automate_lesson", False)),
        lessons_per_module=int(r.get("lessons_per_module", 10)),
        sentences_per_word=dict(spw),
    )


@router.post("/draft", response_model=EditorDraftResponse)
async def save_draft(request: SaveEditorDraftRequest):
    """Create a new editor draft (wizard state)."""
    words_json = json.dumps([w.model_dump() for w in request.words_with_weight])
    sentences_json = json.dumps(request.sentences_per_word)
    sql = """
    INSERT INTO course.editor_draft (
        title, description, lang, to_lang, selected_question_type_ids,
        words_with_weight, step, automate_lesson, lessons_per_module, sentences_per_word
    ) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s::jsonb)
    RETURNING id, created_at, updated_at, title, description, lang, to_lang,
              selected_question_type_ids, words_with_weight, step, automate_lesson, lessons_per_module, sentences_per_word
    """
    rows = await get_query_results(
        sql,
        (
            request.title, request.description, request.lang, request.to_lang,
            request.selected_question_type_ids, words_json, request.step,
            request.automate_lesson, request.lessons_per_module, sentences_json,
        ),
    )
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to create draft")
    return _draft_from_row(rows[0])


@router.get("/drafts", response_model=list[EditorDraftListItem])
async def list_drafts():
    """List editor drafts (for resume)."""
    sql = """
    SELECT id, title, updated_at, step, lang, to_lang
    FROM course.editor_draft
    ORDER BY updated_at DESC
    LIMIT 50
    """
    rows = await get_query_results(sql, ())
    return [
        EditorDraftListItem(
            id=r["id"],
            title=r.get("title") or "",
            updated_at=str(r.get("updated_at", "")),
            step=int(r.get("step", 0)),
            lang=r.get("lang", ""),
            to_lang=r.get("to_lang", ""),
        )
        for r in rows
    ]


@router.get("/draft/{draft_id}", response_model=EditorDraftResponse)
async def get_draft(draft_id: int):
    """Get full draft by id (for resuming)."""
    sql = """
    SELECT id, created_at, updated_at, title, description, lang, to_lang,
           selected_question_type_ids, words_with_weight, step, automate_lesson, lessons_per_module, sentences_per_word
    FROM course.editor_draft
    WHERE id = %s
    """
    rows = await get_query_results(sql, (draft_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Draft not found")
    return _draft_from_row(rows[0])


@router.put("/draft/{draft_id}", response_model=EditorDraftResponse)
async def update_draft(draft_id: int, request: SaveEditorDraftRequest):
    """Update existing draft (save wizard state)."""
    words_json = json.dumps([w.model_dump() for w in request.words_with_weight])
    sentences_json = json.dumps(request.sentences_per_word)
    sql = """
    UPDATE course.editor_draft SET
        updated_at = now(),
        title = %s, description = %s, lang = %s, to_lang = %s,
        selected_question_type_ids = %s, words_with_weight = %s::jsonb, step = %s,
        automate_lesson = %s, lessons_per_module = %s, sentences_per_word = %s::jsonb
    WHERE id = %s
    RETURNING id, created_at, updated_at, title, description, lang, to_lang,
              selected_question_type_ids, words_with_weight, step, automate_lesson, lessons_per_module, sentences_per_word
    """
    rows = await get_query_results(
        sql,
        (
            request.title, request.description, request.lang, request.to_lang,
            request.selected_question_type_ids, words_json, request.step,
            request.automate_lesson, request.lessons_per_module, sentences_json,
            draft_id,
        ),
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Draft not found")
    return _draft_from_row(rows[0])


# --- Lesson wizard: generate questions from sentences, save lesson ---

async def _load_sentence_pair(lang: str, to_lang: str, sentence_id: int, to_id: int) -> tuple[dict, dict] | None:
    """Load sentence from sentence_elements and translation from sentences. Returns (sentence_row, to_row) or None."""
    sql = """
    SELECT l.id, l.lang, l.text, l.word1, l.word2, l.word3, l.word4
    FROM content_raw.sentence_elements l
    WHERE l.lang = %s AND l.id = %s
    """
    rows = await get_query_results(sql, (lang, sentence_id))
    if not rows:
        return None
    sentence_row = dict(rows[0])
    sql_to = """
    SELECT id, lang, text, options
    FROM content_raw.sentences t
    WHERE t.lang = %s AND t.id = %s
    """
    to_rows = await get_query_results(sql_to, (to_lang, to_id))
    if not to_rows:
        return None
    to_row = dict(to_rows[0])
    opts = to_row.get("options")
    to_row["options"] = list(opts) if isinstance(opts, (list, tuple)) and opts else []
    return (sentence_row, to_row)


@router.post("/questions_for_sentences", response_model=GenerateQuestionsResponse)
async def generate_questions_for_sentences(request: GenerateQuestionsRequest):
    """Generate mostly single_choice + ~10% other type (e.g. identify_words) as preview. Plan step 4–5."""
    exercises: list[GeneratedExercisePreview] = []
    seen_text_pairs: set[tuple[str, str]] = set()
    for pair in request.sentences:
        loaded = await _load_sentence_pair(request.lang, request.to_lang, pair.sentence_id, pair.to_id)
        if not loaded:
            continue
        sentence_row, to_row = loaded
        sentence_text = sentence_row.get("text") or ""
        to_text = to_row.get("text") or ""
        text_key = (sentence_text, to_text)
        if text_key in seen_text_pairs:
            continue
        seen_text_pairs.add(text_key)
        options = to_row.get("options") or []
        wrong = list(options) if isinstance(options, (list, tuple)) else []
        audio_link = await _get_audio_link(request.lang, pair.sentence_id)
        exercises.append(GeneratedExercisePreview(
            exercise_type="sentence_single_choice",
            sentence=sentence_text,
            to_sentence=to_text,
            correct_options=[to_text],
            wrong_options=wrong[:6],
            sentence_id=pair.sentence_id,
            to_sentence_id=pair.to_id,
            audio_link=audio_link,
        ))
        words = []
        for k in ("word1", "word2", "word3", "word4"):
            w = sentence_row.get(k)
            if w and w not in words:
                words.append(w)
        if len(words) >= 2 and random.random() < 0.10:
            correct = words[:3] if len(words) >= 3 else words
            exercises.append(GeneratedExercisePreview(
                exercise_type="identify_words_in_speech",
                sentence=sentence_text,
                to_sentence=to_text,
                correct_options=correct,
                wrong_options=[],
                sentence_id=pair.sentence_id,
                to_sentence_id=pair.to_id,
                extra_data={"words": correct},
                audio_link=audio_link,
            ))
    return GenerateQuestionsResponse(word=request.word, exercises=exercises)


@router.post("/save_lesson", response_model=SaveLessonResponse)
async def save_lesson(request: SaveLessonRequest):
    """Save one lesson (one word) with selected exercises. Create course and module if course_id is 0. Plan step 6."""
    course_id = request.course_id
    module_id = request.module_id
    lang = request.lang
    to_lang = request.to_lang
    word = request.word
    title = request.title or word
    n = request.lessons_per_module or 10
    if course_id <= 0:
        sql_course = """
        INSERT INTO content.course (lang, to_lang, title, description)
        VALUES (%s, %s, %s, %s) RETURNING course_id
        """
        rows = await get_query_results(
            sql_course,
            (lang, to_lang, request.course_title or title, request.course_description or ""),
        )
        if not rows:
            raise HTTPException(status_code=500, detail="Failed to create course")
        course_id = rows[0]["course_id"]
        sql_mod = """
        INSERT INTO content.module (course_id, lang, to_lang, title, description)
        VALUES (%s, %s, %s, %s, %s) RETURNING module_id
        """
        mod_rows = await get_query_results(sql_mod, (course_id, lang, to_lang, "Module 1", "Module 1"))
        if not mod_rows:
            raise HTTPException(status_code=500, detail="Failed to create module")
        module_id = mod_rows[0]["module_id"]
    elif module_id <= 0 and course_id > 0:
        count_sql = "SELECT COUNT(*) AS c FROM content.module WHERE course_id = %s"
        cnt = await get_query_results(count_sql, (course_id,))
        mod_num = (cnt[0]["c"] + 1) if cnt else 1
        sql_mod = """
        INSERT INTO content.module (course_id, lang, to_lang, title, description)
        VALUES (%s, %s, %s, %s, %s) RETURNING module_id
        """
        mod_rows = await get_query_results(
            sql_mod, (course_id, lang, to_lang, f"Module {mod_num}", f"Module {mod_num}")
        )
        if not mod_rows:
            raise HTTPException(status_code=500, detail="Failed to create module")
        module_id = mod_rows[0]["module_id"]
    sql_lesson = """
    INSERT INTO content.lesson (course_id, module_id, lang, to_lang, title, description)
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING lesson_id
    """
    lesson_rows = await get_query_results(sql_lesson, (course_id, module_id, lang, to_lang, title, request.description or ""))
    if not lesson_rows:
        raise HTTPException(status_code=500, detail="Failed to create lesson")
    lesson_id = lesson_rows[0]["lesson_id"]
    for ex in request.exercises:
        wrong_options = ex.wrong_options or []
        correct_options = ex.correct_options or [ex.to_sentence]
        sql_ex = """
        INSERT INTO content.exercise (course_id, module_id, lesson_id, lang, to_lang, exercise_type,
        sentence_id, sentence,
        correct_options, to_sentence_id, wrong_options, audio_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await run_query(
            sql_ex,
            (
                course_id, module_id, lesson_id, lang, to_lang, ex.exercise_type,
                ex.sentence_id, ex.sentence or "", correct_options, ex.to_sentence_id, wrong_options,
                ex.audio_link or "",
            ),
        )
    return SaveLessonResponse(course_id=course_id, module_id=module_id, lesson_id=lesson_id)


@router.post("/module_exercises", response_model=ModuleExercisesResponse)
async def module_exercises(request: ModuleExercisesRequest):
    """Generate exercises for all words in a module at once. Flags duplicate translations."""
    sql = """
    SELECT l.id AS id, l.lang, l.text AS sentence, t.text AS translation, t.id AS to_id,
           l.len_elm, l.word1, l.word2, l.word3, l.word4, t.options AS options
    FROM content_raw.sentence_elements l
    JOIN content_raw.translation_links tl ON l.lang = tl.lang AND l.id = tl.id
    JOIN content_raw.sentences t ON tl.to_lang = t.lang AND tl.to_id = t.id
    WHERE tl.lang = %s AND tl.to_lang = %s
      AND (l.root = %s OR l.word1 = %s OR l.word2 = %s OR l.word3 = %s)
    ORDER BY l.len_elm ASC NULLS LAST
    LIMIT %s
    """
    enabled = set(request.question_types) if request.question_types else None
    # Collect all exercises per word before duplicate detection
    word_exercises_raw: list[tuple[str, list[GeneratedExercisePreview]]] = []
    to_id_counts: dict[int, int] = {}

    for word in request.words:
        rows = await get_query_results(
            sql, (request.lang, request.to_lang, word, word, word, word, request.sentences_per_word)
        )
        # Deduplicate rows by (sentence_text, translation_text), picking one randomly
        seen_text_pairs: dict[tuple[str, str], dict] = {}
        for r in rows:
            key = (r.get("sentence") or "", r.get("translation") or "")
            if key not in seen_text_pairs or random.random() < 0.5:
                seen_text_pairs[key] = r
        deduped_rows = list(seen_text_pairs.values())

        exercises: list[GeneratedExercisePreview] = []
        for r in deduped_rows:
            sentence_text = r.get("sentence") or ""
            to_text = r.get("translation") or ""
            to_id = r.get("to_id", 0)
            s_id = r.get("id", 0)
            audio_link = await _get_audio_link(request.lang, s_id)
            if not enabled or "sentence_single_choice" in enabled:
                opts = r.get("options")
                wrong = list(opts)[:6] if isinstance(opts, (list, tuple)) and opts else []
                exercises.append(GeneratedExercisePreview(
                    exercise_type="sentence_single_choice",
                    sentence=sentence_text,
                    to_sentence=to_text,
                    correct_options=[to_text],
                    wrong_options=wrong,
                    sentence_id=s_id,
                    to_sentence_id=to_id,
                    audio_link=audio_link,
                ))
                to_id_counts[to_id] = to_id_counts.get(to_id, 0) + 1
            words_in_s = [r.get(k) for k in ("word1", "word2", "word3", "word4") if r.get(k)]
            if len(words_in_s) >= 2 and (not enabled or "identify_words_in_speech" in enabled):
                correct = words_in_s[:3]
                exercises.append(GeneratedExercisePreview(
                    exercise_type="identify_words_in_speech",
                    sentence=sentence_text,
                    to_sentence=to_text,
                    correct_options=correct,
                    wrong_options=[],
                    sentence_id=s_id,
                    to_sentence_id=to_id,
                    extra_data={"words": correct},
                    audio_link=audio_link,
                ))
        word_exercises_raw.append((word, exercises))

    # Build distractor pool: words_so_far from previous modules + all identify-exercise words in this module
    distractor_pool: list[str] = list(request.words_so_far)
    for _, exercises in word_exercises_raw:
        for ex in exercises:
            if ex.exercise_type == "identify_words_in_speech":
                distractor_pool.extend(ex.correct_options)
    # Deduplicate while preserving order
    seen: set[str] = set()
    distractor_pool_dedup: list[str] = []
    for w in distractor_pool:
        if w not in seen:
            seen.add(w)
            distractor_pool_dedup.append(w)

    # Mark duplicates and assign wrong options for identify exercises
    results = []
    for word, exercises in word_exercises_raw:
        for ex in exercises:
            if ex.exercise_type == "sentence_single_choice" and to_id_counts.get(ex.to_sentence_id, 0) > 1:
                ex.is_duplicate = True
            elif ex.exercise_type == "identify_words_in_speech":
                correct_set = set(ex.correct_options)
                candidates = [w for w in distractor_pool_dedup if w not in correct_set]
                if candidates:
                    ex.wrong_options = random.sample(candidates, min(3, len(candidates)))
        results.append(WordExercisesResult(word=word, exercises=exercises))

    return ModuleExercisesResponse(lang=request.lang, to_lang=request.to_lang, results=results)


@router.get("/course/{course_id}/detail", response_model=CourseDetail)
async def get_course_detail(course_id: int):
    """Return full course tree (modules → lessons → exercises) for review screen."""
    course_rows = await get_query_results(
        "SELECT id, title, description, lang, to_lang FROM content.course WHERE id = %s", (course_id,)
    )
    if not course_rows:
        raise HTTPException(status_code=404, detail="Course not found")
    c = course_rows[0]
    module_rows = await get_query_results(
        "SELECT id, title FROM content.module WHERE course_id = %s ORDER BY id", (course_id,)
    )
    modules = []
    for mod in module_rows:
        lesson_rows = await get_query_results(
            "SELECT id, title FROM content.lesson WHERE module_id = %s ORDER BY id", (mod["id"],)
        )
        lessons = []
        for lesson in lesson_rows:
            ex_rows = await get_query_results(
                """SELECT exercise_id AS id, exercise_type, sentence, sentence_id, to_sentence_id,
                          correct_options, wrong_options
                   FROM content.exercise WHERE lesson_id = %s ORDER BY exercise_id""",
                (lesson["id"],),
            )
            exercises = [
                ExerciseDetail(
                    id=r["id"],
                    exercise_type=r.get("exercise_type") or "",
                    sentence=r.get("sentence") or "",
                    to_sentence="",
                    sentence_id=r.get("sentence_id") or 0,
                    to_sentence_id=r.get("to_sentence_id") or 0,
                    correct_options=list(r.get("correct_options") or []),
                    wrong_options=list(r.get("wrong_options") or []),
                )
                for r in ex_rows
            ]
            lessons.append(LessonDetail(id=lesson["id"], title=lesson["title"] or "", exercises=exercises))
        modules.append(ModuleDetail(id=mod["id"], title=mod["title"] or "", lessons=lessons))
    return CourseDetail(
        id=c["id"],
        title=c.get("title") or "",
        description=c.get("description") or "",
        lang=c["lang"],
        to_lang=c["to_lang"],
        modules=modules,
    )


@router.delete("/course/exercises")
async def delete_exercises(request: DeleteExercisesRequest):
    """Remove exercises by ID (for review screen edits)."""
    if not request.exercise_ids:
        return {"deleted": 0}
    placeholders = ",".join(["%s"] * len(request.exercise_ids))
    await run_query(f"DELETE FROM content.exercise WHERE id IN ({placeholders})", tuple(request.exercise_ids))
    return {"deleted": len(request.exercise_ids)}


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