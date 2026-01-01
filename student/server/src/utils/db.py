from psycopg import AsyncConnection
from psycopg.rows import dict_row
import os
_conn = None
# from aerospike import client
_aerospike_client = None

def get_pg_connection_string(user=None, password=None, db_name=None, host=None, port=None):
    if not user:
        user = os.getenv("POSTGRES_USER", "polyglots")
    if not password:
        password = os.getenv("POSTGRES_PASSWORD", "polyglots")
    if not db_name:
        db_name = os.getenv("POSTGRES_DB", "polyglots")  
    if not host:
        host = os.getenv("POSTGRES_HOST", "localhost")  
    if not port:
        port = os.getenv("POSTGRES_PORT", "5432")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


async def get_pg_con():
    global _conn
    connection_string = get_pg_connection_string()

    if not _conn:
        _conn =  await AsyncConnection.connect(
            connection_string, 
            row_factory=dict_row, 
            autocommit=True,
        ) 
    return _conn

async def close_pg_con():
    global _conn
    if _conn:
        await _conn.close()
        _conn = None

def get_current_customer():
    return f"polyglots"



async def get_query_results(sql:str, params:tuple)-> list:
    conn = await get_pg_con()
    cursor = conn.cursor()
    # print(sql)
    # print(params) 
    try:
        res = await cursor.execute(sql, params)
    except Exception as e:
        print(f"Error executing SQL: {sql}")
        print(e)
        return []
    try:
        results = await cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error fetching results: {sql}")
        print(e)
        return [] 


async def run_query(sql:str, params:tuple)-> bool:
    conn = await get_pg_con()
    cursor = conn.cursor()
    # print(sql)
    # print(len(params)) 
    # print(params, len(params)) 
    try:
        res = await cursor.execute(sql, params)
        await conn.commit()
        return True
    except Exception as e:
        print(f"Error executing SQL: {sql}")
        print(e)
        return False


# def get_aerospike_client():
#     global _aerospike_client
#     if not _aerospike_client:
#         _aerospike_client = client.Client(os.getenv("AEROSPIKE_HOST"), os.getenv("AEROSPIKE_PORT"))
#     return _aerospike_client