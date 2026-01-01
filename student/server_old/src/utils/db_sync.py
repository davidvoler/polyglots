import psycopg 
from psycopg.rows import dict_row
import os
_conn_sync = None


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


def get_pg_con():
    global _conn_sync
    connection_string = get_pg_connection_string()

    if not _conn_sync:
        _conn_sync =  psycopg.connect(
            connection_string, 
            row_factory=dict_row, 
            autocommit=True,
        ) 
    return _conn_sync

def close_pg_con():
    global _conn_sync
    if _conn_sync:
        _conn_sync.close()
        _conn_sync = None

def get_current_customer():
    return f"polyglots"



def get_query_results(sql:str, params:tuple)-> list:
    conn = get_pg_con()
    cursor = conn.cursor()

    # print(sql)
    # print(params) 
    try:
        res = cursor.execute(sql, params)
        conn.commit()
    except Exception as e:
        print(f"Error executing SQL: {sql}")
        print(e)
        return []
    try:
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error fetching results: {sql}")
        print(e)
        return [] 


def run_query(sql:str, params:tuple)-> bool:
    conn = get_pg_con()
    cursor = conn.cursor()
    try:
        res = cursor.execute(sql, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error executing SQL: {sql}")
        print(e)
        return False
