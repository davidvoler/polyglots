from utils.db import  get_query_results, run_query
import asyncio

langs = ["ar", "de", "el", "es", "fr", "he", "it", "pt", "cs","hi", "pt-PT", "ru", "zh-Hans", "ja"]

async def update_dialogues_from_line():
    for lang in langs:
        sql = f"""
        select * from polyglots_quiz.steps
        where lang = %s 
        """
        params = (lang,)
        results = await get_query_results(sql, params)
        for r in results:
            step_id = r.get("step_id")
            dialogues = r.get("dialogues", [])
            lines = r.get("lines", [])
            if not dialogues :
                dialogues = []
            if  not lines:
                continue
            for l in lines:
                dialogues.append(l.split("_")[0])
            if len(dialogues) > 0:
                sql = f"""
                update polyglots_quiz.steps
                set dialogues = %s 
                where step_id = %s
                and lang = %s
                """
                params = (dialogues, step_id, lang)
                print("Updating dialogues for step_id:", step_id, "lang:", lang, "dialogues:", dialogues)
                await run_query(sql, params)


asyncio.run(update_dialogues_from_line())