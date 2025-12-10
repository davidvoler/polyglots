from psycopg import AsyncConnection
from psycopg.rows import dict_row
from cityhash import CityHash32
from common.utils.language import get_lang3, get_lang2
import asyncio

# async def create_batch_id(client:AsyncConnection):
#     batch_id = str(guid())
#     insert_sql = """INSERT INTO content_raw.batch_status (action, batch_id) VALUES (%s, %s)"""
#     cursor = client.cursor()
#     await cursor.execute(insert_sql, ("export_existing_corpus", batch_id))
#     return batch_id

async def get_client(old = False):

    if old:
        return await AsyncConnection.connect(
            "postgresql://polyglots:polyglots@localhost:5432/polyglots",
            row_factory=dict_row,
            autocommit=True,
        )
    else:
        return await AsyncConnection.connect(
            "postgresql://polyglots:polyglots@localhost:5433/polyglots",
            row_factory=dict_row,
            autocommit=True,
        )

async def get_old_data(lang:str):
    client = await get_client(old=True)
    get_data_sql = """SELECT * from tatoeba.parts where lang = %s"""
    cursor = client.cursor()
    res = await cursor.execute(get_data_sql, (lang,))
    return await cursor.fetchall()


async def export_polyglot(lang:str):
    data = await get_old_data(lang)
    new_client = await get_client(old=False)
    cursor = new_client.cursor()
    corpus = 'tatoeba'
    for row in data:
        text = row.get("text").strip()
        cityhash_id = CityHash32(text)
        insert_sql = """INSERT INTO content_raw.sentences (lang, corpus, id, text,gen) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (lang, id) DO UPDATE SET text = EXCLUDED.text
        """
        await cursor.execute(insert_sql, ('ja', corpus, cityhash_id, text, False))



async def export_all_tatoeba():
    lng3 = list_langs3()
    for l3 in lng3:
        lng2 = get_lang2(l3)
        print(f"Exporting {lng2} from {l3}")


if __name__ == "__main__":
    asyncio.run(export_polyglot("jpn"))