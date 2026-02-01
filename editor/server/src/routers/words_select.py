from fastapi import APIRouter
from pydantic import BaseModel
from models.word_select import WordSelectRequest, ModuleWords, WordSelect
from generators.module_words import select_module_words, select_greetings_words, select_corpus_words

router = APIRouter()


class WordWithWeight(BaseModel):
    word: str
    weight: int


class SubmitWordsRequest(BaseModel):
    lang: str
    to_lang: str = ""
    words: list[WordWithWeight]


@router.post("/")
async def select_words_module(req: WordSelectRequest) -> list[ModuleWords]:
    return await select_module_words(req)


@router.post("/greeting_words")
async def greeting_words(req: WordSelectRequest) -> list:
    """Step 2a: Return greeting/polite words (WordSelect with greeting=True)."""
    return [w.model_dump() for w in await select_greetings_words(req)]


@router.post("/all_words")
async def all_words(req: WordSelectRequest) -> list:
    """Correct Wizard step 3: Return greeting words + corpus words (all WordSelect elements)."""
    greeting_list = await select_greetings_words(req)
    corpus_list = await select_corpus_words(req)
    return [w.model_dump() for w in greeting_list] + [w.model_dump() for w in corpus_list]


@router.post("/submit_words")
async def submit_words(req: SubmitWordsRequest):
    """Correct Wizard step 8: Accept list of words with weight (sort order)."""
    return {"lang": req.lang, "to_lang": req.to_lang, "count": len(req.words), "words": [w.model_dump() for w in req.words]}