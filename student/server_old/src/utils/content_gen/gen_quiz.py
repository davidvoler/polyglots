from utils.db import get_query_results, run_query
import random

def _get_by_stop_words(lang:str, stop_words, c_count:int):
    min_count = c_count - (int(c_count/5))
    max_count = c_count+(int(c_count/5))
    sql = f"""
        SELECT sentence FROM tatoeba.prepared_sentences
        WHERE 
    """
    random.shuffle(options)
    return options[:6]

def _get_by_first(lang:str, first:str, c_count:int):
    min_count = c_count - (int(round(c_count/5)))
    max_count = c_count+(int(round(c_count/5)))
    sql = f"""
        SELECT sentence FROM 
        WHERE 
    """
    options = []
    return options[:6]

def _get_by_words(lang:str,,words:list, w_count:int, min_count=2):
    sql = f"""
        SELECT sentence FROM 
        WHERE 
    """
    return []

def _get_by_propn(lang:str,propn:list, w_count:int, min_count=1):
    min_count = max(w_count-2, 3)
    max_count = w_count+2
    sql = f"""
        SELECT sentence FROM 
        WHERE 
    """


def _get_by_root(lang:str,root:str, c_count:int):
    min_count = c_count - (int(c_count/4))
    max_count = c_count+(int(c_count/4))
    sql = f"""
        SELECT sentence FROM 
        WHERE 
    """


def _get_by_w_count_fixed(lang:str, w_count:int):
    r = random.randint(1000)
    sentences = client[db][collection].find({"w_count":w_count}, {"_id":1}).skip(r).limit(100)
    options = [o.get("_id") for o in sentences]
    random.shuffle(options)
    return options[:10]

def _get_by_w_count(lang:str, w_count:int):
    min_count = max(w_count-1, 2)
    max_count = w_count+1
    r = random.randint(1000)
    sentences = client[db][collection].find({"w_count":{"$gte":min_count, "$lte":max_count}}, {"_id":1}).skip(r).limit(50)
    options = [o.get("_id") for o in sentences]
    random.shuffle(options)
    return options[:6]


def _get_by_w_last_c(lang:str,last_c:str, w_count:int):
    min_count = max(w_count-1, 3)
    max_count = w_count+2
    sentences = client[db][collection].find({"$and":[{"last_c":last_c},{"w_count":{"$gte":min_count, "$lte":max_count}}]}, {"_id":1})
    options = [o.get("_id") for o in sentences]
    random.shuffle(options)
    return options[:6]


def _get_by_w_first_c(lang:str,first_c:str, w_count:int):
    min_count = min(w_count-1, 3)
    max_count = w_count+2
    sentences = client[db][collection].find({"$and":[{"first_c":first_c},{"w_count":{"$gte":min_count, "$lte":max_count}}]}, {"_id":1})
    options = [o.get("_id") for o in sentences]
    random.shuffle(options)
    return options[:6]

def _get_by_random(lang:str, collection:str):
    r = random.randint(1,3000)
    sentences = client[db][collection].find({}, {"_id":1}).skip(r).limit(200)
    options = [o.get("_id") for o in sentences]
    random.shuffle(options)
    return options[:7]

def get_by_multiple_elements(lang:str,sentence:dict, options:list=[]):
    words = sentence.get("words")
    all_words = sentence.get("all_words")
    stop_words = sentence.get("stop_words")
    c_count = sentence.get("c_count")
    root = sentence.get("root")
    first = sentence.get("first")
    last_c = sentence.get("last_c")
    first_c = sentence.get("first_c")
    w_count = sentence.get("w_count", 1)
    propn = sentence.get("propn", [])
    if w_count <= 2:
        options += _get_by_w_count_fixed(lang,w_count)
        options = list(set(options))
        random.shuffle(options)
        return options[:7]
    options += _get_by_words(lang, words, w_count,min_count=3)[:6]
    options += _get_by_words(lang, words, w_count,min_count=2)[:5]
    options += _get_by_words(lang, words, w_count,min_count=1)[:4]
    options += _get_by_first(lang, first, c_count)[:3]
    options += _get_by_root(lang, root, c_count)[:3]
    if len(propn) > 0:
        options += _get_by_propn(lang, propn, w_count)[:3]
    
    options += _get_by_w_last_c(lang, last_c, w_count)[:4]
    options += _get_by_w_first_c(lang, first_c, w_count)[:4]
    options = list(set(options))
    random.shuffle(options)
    if len(options) > 9:
        return options
    options += _get_by_w_count(lang, w_count)[:5]
    if len(options) < 6:
        options += _get_by_random(lang)[:6]
    random.shuffle(options)
    return options
    




def get_quiz(db, lang,  collection, field,  overwrite=False, min_options=7):
    collection = f"{collection}_{lang}"
    sentences = client[db][collection].find()
    for s in sentences:
        if overwrite:
            options = []
        else:
            options = s.get("options", [])
        if len(options) >= min_options:
            continue
        options = get_by_multiple_elements(lang, s, options)
        try:
            options.remove(s.get("_id"))
        except:
            pass
        print(s.get(field))
        for i in range(len(options)):
            print(i+1, ":", options[i])
        client[db][collection].update_one(
            {"_id": s.get("_id")},
            {"$set": {"options": options, "o_count": len(options)}}
        )

def get_quiz_new(lang, field="sentence",  overwrite=False, min_options=6):
    sentences = client[db][collection].find()
    for s in sentences:
        if overwrite:
            options = []
        else:
            options = s.get("options", [])
        if len(options) >= min_options:
            continue
        options = get_by_multiple_elements(lang, s, options)
        try:
            options.remove(s.get("_id"))
        except:
            pass
        print(s.get(field))
        for i in range(len(options)):
            print(i+1, ":", options[i])
        client[db][collection].update_one(
            {"_id": s.get("_id")},
            {"$set": {"options": options, "o_count": len(options)}}
        )

def get_words_quiz(db, lang,  collection, field,  overwrite=False, min_options=5):
    collection = f"{collection}_{lang}"
    sentences = client[db][collection].find()
    for s in sentences:
        if overwrite:
            options = []
        else:
            options = s.get("options", [])
        if len(options) >= min_options:
            continue
        options = options + _get_by_random(db, collection)
        try:
            options.remove(s.get("_id"))
        except:
            pass
        options = list(set(options))
        print(s.get(field))
        for i in range(len(options)):
            print(i+1, ":", options[i])

        client[db][collection].update_one(
            {"_id": s.get("_id")},
            {"$set": {"options": options, "o_count": len(options)}}
        )



