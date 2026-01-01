from utils.db import get_pg_con, run_query, get_aerospike_client
from aerospike_helpers.operations import map_operations, operations
import aerospike
from models.results import Results
import datetime
import time
import random
from models.user_vocab import UserVocab
from models.user_data import UserData


def get_user_data(user_id:str, lang:str) -> UserData:
    client = get_aerospike_client()
    as_key = ('tatoeba_users', 'user_data', f'{user_id}:{lang}')
    _,_,bins = client.get(as_key)
    return UserData(**bins)

def save_uv(uv:UserVocab):
    as_key = ('tatoeba_users', 'user_vocab', f'{uv.user_id}:{uv.lang}')
    client = get_aerospike_client()
    client.put(as_key, uv.model_dump())

def get_uv(user_id:str, lang:str):
    as_key = ('tatoeba_users', 'user_vocab', f'{user_id}:{lang}')
    client = get_aerospike_client()
    _,_,bins = client.get(as_key)
    return UserVocab(**bins)



def get_or_create_user_data(user_id:str, lang:str) -> UserData:
    user_data = get_user_data(user_id, lang)
    if not user_data:
        user_data = UserData(user_id=user_id, lang=lang)
        save_user_data(user_data)
    return user_data

def save_user_data(user_data:UserData):
    as_key = ('tatoeba_users', 'user_data', f'{user_data.user_id}:{user_data.lang}')
    client = get_aerospike_client()
    client.put(as_key, user_data.model_dump())