from webbrowser import get
from utils.db import get_query_results, run_query, get_pg_con_specific
from cityhash import CityHash32
from utils.languages import list_langs3, list_langs2, get_lang3, get_lang2 
import asyncio


async def get_old_data_tatoeba(lang:str):
    sql = """
    SELECT text, recording from tatoeba.parts_new where lang = %s
    """
    return await get_query_results(sql, (lang,))

async def get_old_data_polyglots(lang:str, to_lang:str):
    sql = """select text, recording from polyglots_quiz.parts where lang = %s
    """
    return await get_query_results(sql, (lang, to_lang))



async def export_polyglot(lang:str):
    data = await get_old_data_tatoeba(lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    lang2 = get_lang2(lang)
    audio_engine = 'azure'
    base_path = f"/{lang2}/{lang2}"
    for row in data:
        text_lang = row.get("text_lang").strip()
        cityhash_id_lang = CityHash32(text_lang)
        recording = row.get_recording("recording", "")
        if recording:
            full_recording_path = f"{base_path}/{recording}"
            insert_sql = """INSERT INTO content_raw.audio (lang, id,recording,audio_engine) VALUES (%s, %s, %s, %s)
            ON CONFLICT (lang, id) DO NOTHING
            """
            await run_query(insert_sql, (lang2, cityhash_id_lang, full_recording_path, audio_engine), conn=new_client)


async def export_tatoeba(lang:str):
    data = await get_old_data_tatoeba(lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    lang2 = get_lang2(lang)
    audio_engine = 'google'
    base_path = f"/{lang2}/{lang}"
    for row in data:
        text_lang = row.get("text_lang").strip()
        cityhash_id_lang = CityHash32(text_lang)
        recording = row.get_recording("recording", "")
        if recording:
            full_recording_path = f"{base_path}/{recording}"
            insert_sql = """INSERT INTO content_raw.audio (lang, id,recording,audio_engine) VALUES (%s, %s, %s, %s)
            ON CONFLICT (lang, id) DO NOTHING
            """
            await run_query(insert_sql, (lang2, cityhash_id_lang, full_recording_path, audio_engine), conn=new_client)






async def import_recording_tatoeba():
    lng3 = list_langs3()
    for lfrom in lng3:
        for lto in lng3:
            if lfrom == lto:
                continue
            print(f"Exporting  links {lfrom} to {lto}")
            # await export_tatoeba(lfrom, lto)
            await export_polyglot(get_lang2(lfrom), get_lang2(lto))

if __name__ == "__main__":

    asyncio.run(import_recording_tatoeba())
    # asyncio.run(export_tatoeba_secondary('ces', 'eng', 'heb'))