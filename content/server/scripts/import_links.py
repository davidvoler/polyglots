from webbrowser import get
from utils.db import get_query_results, run_query, get_pg_con_specific
from cityhash import CityHash32
from utils.languages import list_langs3, list_langs2, get_lang3, get_lang2 
import asyncio


async def get_old_data_tatoeba(lang:str, to_lang:str):
    sql = """
    SELECT p_lang.text as text_lang, p_to_lang.text as text_to_lang from 
    tatoeba.parts p_lang
    join tatoeba.links l on p_lang.part_id = l.id 
    join tatoeba.parts p_to_lang on l.to_id = p_to_lang.part_id
    where p_lang.lang = %s and p_to_lang.lang = %s 
    
    """
    return await get_query_results(sql, (lang, to_lang))

async def get_old_data_polyglots(lang:str, to_lang:str):
    sql = """SELECT p_lang.text as text_lang, p_to_lang.text as text_to_lang from polyglots_quiz.parts p_lang
    join polyglots_quiz.parts p_to_lang on p_lang.part_id = p_to_lang.part_id
    where p_lang.lang = %s and p_to_lang.lang = %s 
    """
    return await get_query_results(sql, (lang, to_lang))

async def export_polyglot(lang:str, to_lang:str):
    data = await get_old_data_polyglots(lang,to_lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    corpus = 'gen_dialogue'
    for row in data:
        text_lang = row.get("text_lang").strip()
        text_to_lang = row.get("text_to_lang").strip()
        cityhash_id_lang = CityHash32(text_lang)
        cityhash_id_to_lang = CityHash32(text_to_lang)
        insert_sql = """INSERT INTO content_raw.translation_links (lang, id,to_lang,to_id,corpus,machine,direct) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (lang, id, to_lang, to_id) DO NOTHING
        """
        await run_query(insert_sql, (lang, cityhash_id_lang, to_lang,cityhash_id_to_lang, corpus, True, False), conn=new_client)

async def export_tatoeba(lang:str, to_lang:str):
    data = await get_old_data_tatoeba(lang, to_lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    lang2 = get_lang2(lang)
    to_lang2 = get_lang2(to_lang)
    corpus = 'tatoeba'
    for row in data:
        text_lang = row.get("text_lang").strip()
        text_to_lang = row.get("text_to_lang").strip()
        cityhash_id_lang = CityHash32(text_lang)
        cityhash_id_to_lang = CityHash32(text_to_lang)
        insert_sql = """INSERT INTO content_raw.translation_links (lang, id,to_lang,to_id,corpus,machine,direct) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (lang, id, to_lang, to_id) DO NOTHING
        """
        await run_query(insert_sql, (lang2, cityhash_id_lang, to_lang2,cityhash_id_to_lang, corpus, False, True), conn=new_client)



async def get_old_data_tatoeba_secondary(lang:str, to_lang:str, secondary_lang:str):
    sql = """
        SELECT l.id, l2.to_id, max(p.text) as text_lang, max(p2.text) as text_to_lang 
        FROM tatoeba.parts p
        join tatoeba.links l on l.id = p.part_id
        join tatoeba.links l2 on l.to_id = l2.id
        join tatoeba.parts p2 on l2.to_id = p2.part_id  
        where l.lang=%s and l.to_lang=%s and l2.lang= %s and l2.to_lang = %s
        group by 1,2    
    """
    print(sql, (lang, to_lang, secondary_lang))
    return await get_query_results(sql, (lang, to_lang,to_lang, secondary_lang))


async def export_tatoeba_secondary(lang:str, to_lang:str, secondary_lang:str):
    data = await get_old_data_tatoeba_secondary(lang, to_lang, secondary_lang=secondary_lang)
    new_client = await get_pg_con_specific(host="localhost", port="5433", db_name="polyglots", user="polyglots", password="polyglots")
    lang2 = get_lang2(lang)
    to_lang2 = get_lang2(to_lang)
    secondary_lang2 = get_lang2(secondary_lang)
    corpus = 'tatoeba'
    row_count = 0
    for row in data:
        row_count += 1
        text_lang = row.get("text_lang").strip()
        text_to_lang = row.get("text_to_lang").strip()
        cityhash_id_lang = CityHash32(text_lang)
        cityhash_id_to_lang = CityHash32(text_to_lang)
        insert_sql = """INSERT INTO content_raw.translation_links (lang, id,to_lang,to_id,corpus,machine,direct) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (lang, id, to_lang, to_id) DO NOTHING
        """
        await run_query(insert_sql, (lang2, cityhash_id_lang, secondary_lang2,cityhash_id_to_lang, corpus, False, False), conn=new_client)
        print(text_lang, cityhash_id_lang, secondary_lang2,cityhash_id_to_lang, text_to_lang)

    print(f"Exported {row_count} rows for {lang} to {to_lang} and {secondary_lang}")



async def export_all_tatoeba():
    lng3 = list_langs3()
    for lfrom in lng3:
        for lto in lng3:
            if lfrom == lto:
                continue
            print(f"Exporting  links {lfrom} to {lto}")
            # await export_tatoeba(lfrom, lto)
            await export_polyglot(get_lang2(lfrom), get_lang2(lto))

if __name__ == "__main__":
    # asyncio.run(export_all_tatoeba())
    asyncio.run(export_tatoeba_secondary('ces', 'eng', 'heb'))