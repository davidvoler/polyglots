from utils.db import get_query_results, run_query, get_pg_con_specific
from cityhash import CityHash32
from utils.languages import list_langs3, list_langs2, get_lang3, get_lang2 
import asyncio
import json

async def get_old_data_tatoeba(lang:str):
    sql = """SELECT * from tatoeba.parts where lang = %s"""
    print(sql, (lang,))
    return await get_query_results(sql, (lang,))

async def get_old_data_polyglots(lang:str):
    sql = """SELECT * from polyglots_quiz.parts where lang = %s"""
    return await get_query_results(sql, (lang,))

async def export_polyglot(lang:str):
    data = await get_old_data_polyglots(lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    corpus = 'gen_dialogue'
    for row in data:
        text = row.get("text").strip()
        cityhash_id = CityHash32(text)
        options = row.get("options")
        print("type(options)", type(options))
        insert_sql = """update content_raw.sentence_elements set options = %s where lang = %s and id = %s
        """
        await run_query(insert_sql, (options, lang, cityhash_id), conn=new_client)
        print(f"Exporting {lang}  - {cityhash_id} - {options} ")

async def export_tatoeba(lang:str):
    data = await get_old_data_tatoeba(lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    lang2 = get_lang2(lang)
    corpus = 'tatoeba'
    for row in data:
        text = row.get("text").strip()
        cityhash_id = CityHash32(text)
        options = row.get("options")
        insert_sql = """update content_raw.sentence_elements set options = %s where lang = %s and id = %s
        """
        await run_query(insert_sql, (options, lang2, cityhash_id), conn=new_client)
        print(f"Exporting {lang2}  - {cityhash_id} - {options} ")


async def export_all_tatoeba():
    lng3 = list_langs3()
    for l3 in lng3:
        print(f"Exporting {l3}")
        lng2 = get_lang2(l3)
        await export_tatoeba(l3)
        await export_polyglot(lng2)

async def export_all_elements():
    # await export_tatoeba('jpn')
    await export_polyglot('ja')
if __name__ == "__main__":
    # asyncio.run(export_all_tatoeba())
    asyncio.run(export_all_elements())