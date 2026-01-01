import asyncio
from export.export import *
from utils.db import get_pg_con, close_pg_con
from export.link_sql import get_quiz
from models.user_vocab import UserVocab




async def main():
    
    
    # for lang in ["ar", "de", "el",  "fr", "he", "it", "ja"]:
    #     fields = [
    #     Field(mongo_name="_id", pg_name="id", lower=True),
    #     Field(mongo_name="lang", pg_name="lang", default=lang),
    #     Field(mongo_name="sentence", pg_name="text"),
    #     ]

    #     await export_collection("subjects", f"sentences_{lang}", "polyglots_content", "unique_sentences",
    #                        fields)

   
    # fields = [
    #     Field(mongo_name="ranked", pg_name="words"),
    #     Field(mongo_name="text", pg_name="text"),
    #     Field(mongo_name="rec", pg_name="recording"),
    #     Field(mongo_name="options", pg_name="options"),
    #     ]

    # await export_collection_inline_params("quiz", f"parts", "polyglots_quiz", "parts", fields)
    # await get_quiz("en", "de")

    # await export_collection("polyglots", "quiz_questions", "polyglots_quiz", "questions", ["question_id", "question"], {"customer_id": "polyglots"})
    # await export_collection("polyglots", "quiz_answers", "polyglots_quiz", "answers", ["answer_id", "answer"], {"customer_id": "polyglots"})
    # await export_collection_dialogue("quiz","dialogues")
    # await export_collection_dialogue_lines("quiz","dialogue_lines")
    # await export_collection_tags("quiz", "tags")
    # await export_collection_dialogue("quiz","dialogues")` 
    # await  add_words_to_dialogues()
    # await step_add_words()
    # await add_dialogues_to_step()
    # await add_structure_to_step()
    # await add_parts_to_step()
    # await add_lines_to_step()
    await close_pg_con()    






asyncio.run(main())




# 



