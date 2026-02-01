from fastapi import APIRouter
from models.word_select import WordSelectRequest, ModuleWords, WordSelect
from generators.module_words import select_module_words, select_greetings_words, select_corpus_words

router = APIRouter()


@router.post("/")
async def select_words_module(req: WordSelectRequest) -> list[WordSelect]:
    return await select_corpus_words(req)


@router.post("/greeting_words")
async def greeting_words(req: WordSelectRequest) -> list[WordSelect]:
    """Step 2a: Return words the user may already know (greetings, polite words) for the given lang."""
    return await select_greetings_words(req)



@router.post("/all_words")
async def all_words(req: WordSelectRequest) -> list[WordSelect]:
    """Step 2a: Return words the user may already know (greetings, polite words) for the given lang."""
    greeting_words = await select_greetings_words(req)
    all_words = await select_corpus_words(req)
    return greeting_words + all_words