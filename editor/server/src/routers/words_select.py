from fastapi import APIRouter
from models.word_select import WordSelectRequest, ModuleWords
from generators.module_words import select_module_words

router = APIRouter()


@router.post("/")
async def select_words_module(req:WordSelectRequest)->list[ModuleWords]:
    return await select_module_words(req)
