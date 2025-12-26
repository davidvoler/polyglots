from generators.module_words import get_all_words_by_sentences_len
import asyncio
import os

os.environ["POSTGRES_PORT"] = "5433"  



async def get_words():
    modules = await get_all_words_by_sentences_len('ja')
    for m in modules:
        print(m)


if __name__ == '__main__':
    asyncio.run(get_words())