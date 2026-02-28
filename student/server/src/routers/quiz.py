import random
from fastapi import APIRouter, HTTPException
from models.quiz import QuizRequest, Quiz, QuizType, Sentence, Option
from utils.db import get_query_results

router = APIRouter()


async def _load_exercises(where_clause: str, params: tuple) -> list[Sentence]:
    """Load exercises from content.exercise and convert to Sentence objects."""
    sql = f"""
    SELECT exercise_id, exercise_type, sentence, correct_options, wrong_options,
           audio_link, sentence_id, to_sentence_id
    FROM content.exercise
    WHERE {where_clause}
    ORDER BY exercise_id
    """
    rows = await get_query_results(sql, params)
    sentences = []
    for r in rows:
        exercise_type = r.get("exercise_type") or "sentence_single_choice"
        correct_options = r.get("correct_options") or []
        wrong_options = r.get("wrong_options") or []

        if isinstance(correct_options, str):
            correct_options = [correct_options]
        if isinstance(wrong_options, str):
            wrong_options = [wrong_options]

        # Build options list: correct + wrong, shuffled
        options = []
        for opt in correct_options:
            options.append(Option(option=opt, correct=True))
        for opt in wrong_options:
            options.append(Option(option=opt, correct=False))
        random.shuffle(options)

        # For identify_words exercises, words = correct_options
        words = list(correct_options) if exercise_type == "identify_words_in_speech" else []

        sentences.append(Sentence(
            sentence=r.get("sentence") or "",
            options=options,
            words=words,
            sentence_id=str(r.get("exercise_id", 0)),
            sound=r.get("audio_link") or "",
            exercise_type=exercise_type,
        ))
    return sentences


async def get_lesson_quiz(req: QuizRequest) -> Quiz:
    sentences = await _load_exercises("lesson_id = %s", (req.lesson_id,))
    return Quiz(
        lang=req.lang,
        to_lang=req.to_lang,
        user_id=req.user_id,
        quiz_type=req.quiz_type,
        course_id=req.course_id,
        module_id=req.module_id,
        lesson_id=req.lesson_id,
        sentences=sentences,
    )


async def get_refresh_module_quiz(req: QuizRequest) -> Quiz:
    sentences = await _load_exercises("module_id = %s", (req.module_id,))
    return Quiz(
        lang=req.lang,
        to_lang=req.to_lang,
        user_id=req.user_id,
        quiz_type=req.quiz_type,
        course_id=req.course_id,
        module_id=req.module_id,
        lesson_id=req.lesson_id,
        sentences=sentences,
    )


async def get_refresh_course_quiz(req: QuizRequest) -> Quiz:
    sentences = await _load_exercises("course_id = %s", (req.course_id,))
    return Quiz(
        lang=req.lang,
        to_lang=req.to_lang,
        user_id=req.user_id,
        quiz_type=req.quiz_type,
        course_id=req.course_id,
        module_id=req.module_id,
        lesson_id=req.lesson_id,
        sentences=sentences,
    )


async def get_refresh_all_quiz(req: QuizRequest) -> Quiz:
    sentences = await _load_exercises("lang = %s AND to_lang = %s", (req.lang, req.to_lang))
    return Quiz(
        lang=req.lang,
        to_lang=req.to_lang,
        user_id=req.user_id,
        quiz_type=req.quiz_type,
        course_id=req.course_id,
        module_id=req.module_id,
        lesson_id=req.lesson_id,
        sentences=sentences,
    )


@router.post("/get_quiz", response_model=Quiz)
async def r_get_quiz(req: QuizRequest) -> Quiz:
    match req.quiz_type:
        case QuizType.lesson:
            return await get_lesson_quiz(req)
        case QuizType.refresh_module:
            return await get_refresh_module_quiz(req)
        case QuizType.refresh_course:
            return await get_refresh_course_quiz(req)
        case QuizType.refresh_all:
            return await get_refresh_all_quiz(req)
        case _:
            raise HTTPException(status_code=400, detail="Invalid quiz type")
