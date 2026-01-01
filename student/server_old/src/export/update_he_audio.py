import psycopg 
from psycopg.rows import dict_row
import hashlib
import os

_conn_sync = None


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

def get_sha1_hash(text: str) -> str:
    test = text.upper()
    text_bytes = test.encode('utf-8')
    return hashlib.sha1(text_bytes).hexdigest()

def record_sentence(text:str, gender:str, part_id:int):
    fname = f"he_{get_sha1_hash(text)}.mp3"
    sql = "update polyglots_quiz.parts set recording = %s where part_id = %s and lang = 'he'"
    run_query(sql, (fname, part_id))


def record_sentence_lines(text:str, gender:str, part_id:int):
    fname = f"he_{get_sha1_hash(text)}.mp3"
    sql = "update polyglots_quiz.dialogue_line set recording = %s where dialogue_line = %s and lang = 'he'"
    run_query(sql, (fname, part_id))


def update_he_audio():
    sql = "SELECT * FROM polyglots_quiz.parts where  lang = 'he' order by part_id"
    data = get_query_results(sql, None)
    for d in data:
        text = d.get('text', '')
        print(text)
        part_id = d.get('part_id', 0)
        gender = None
        if not text or not part_id:
            continue
        record_sentence(text=text, gender=None, part_id=part_id)
            
def update_he_audio_lines():
    sql = "SELECT * FROM polyglots_quiz.dialogue_line where lang = 'he' order by dialogue_id"
    data = get_query_results(sql, None)
    for d in data:
        text = d.get('text', '')
        print(text)
        part_id = d.get('dialogue_line', '')
        gender = None
        if not text or not part_id:
            continue
        record_sentence_lines(text=text, gender=None, part_id=part_id)

update_he_audio()
update_he_audio_lines()


