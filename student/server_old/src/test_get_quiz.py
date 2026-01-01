import asyncio
from export.export import export_collection, Field, export_collection_inline, export_collection_inline_params
from utils.db import get_pg_con, close_pg_con
from export.link_sql import get_quiz
from models.user_vocab import UserVocab
from utils.quiz.quiz_logic import get_user_quiz
from models.modes import PracticeMode
import time 


async def main():
    from server.src.utils.quiz.old.quiz_query import get_step_words
    for i in range(1):
        uv = UserVocab(
                user_id='aaaa',
                customer_id = 'polyglots',
                lang = "de",
                to_lang= "en",
                step = 30,
                last_mode = PracticeMode.structure
            )
        print(await get_step_words(uv))
        start = time.time()
        data = await get_user_quiz(uv=uv, mark=0.9)
        print (f"Time taken: {time.time() - start}")
        for d in data:
            print(d.get("text"))
 






asyncio.run(main())




# 



