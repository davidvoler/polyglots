f''' Cahced data for a user
We can save the data into a cache db like redis or aerospike
Aerospike is easier as we have more functionality 
All this data is saved in a the Journal as well but calling the journal would require
a lot of queries 

Another good reason to use a cache db
1. we can expire the data after a certain time
2. we can update multiple field with resonable cost
3. we can keep a single key per user and get all the data in one api call

cache data structure:
user_id:str,
lang:str,
words:{
    'watched': {
        'mark': float,
        'times': int,
        'last_time': datetime,
    }, 
    'learned': {
        'mark': float,
        'times': int,
        'last_time': datetime,
    },
    'forgot': {
}
parts:{
    '12203': {
        'mark': float,
        'times': int,
        'last_time': datetime,
    },
    '12204': {
        'mark': float,
        'times': int,
        'last_time': datetime,
    },
},
branches:{
    'key1': {
        'mark': float,
        'times': int,
        'last_time': datetime,
    },
    'key2': {
        'mark': float,
        'times': int,
        'last_time': datetime,
    },
},
}


'''
from models.results import ResultsBranch
from aerospike import client


def update_cache_data(results:ResultsBranch):
    """ update the cache data
    """
    pass

def get_cache_data(user_id:str, lang:str):
    """ get the cache data
    """
    pass
    



def get_cache_user_words(user_id:str, lang:str):
    """ get from a cache users latest words and mark
    """
    pass 

def get_cache_user_parts(user_id:str, lang:str):
    """ get from a cache users latest words and mark
    """
    pass 


def get_cache_user_branch(user_id:str, lang:str):
    """ get from a cache users branches
    """
    pass 



def save_cache_user_word(user_id:str, lang:str):
    """ get from a cache users branches
    """
    pass 


def save_cache_user_part(user_id:str, lang:str):
    """ get from a cache users branches
    """
    pass 

def save_cache_user_branch(user_id:str, lang:str):
    """ get from a cache users branches
    """
    pass 
def update_cache_data():
    pass