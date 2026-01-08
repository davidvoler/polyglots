from utils.db import get_query_results, run_query
import json
import random

def _load_elements(folder, fname):
    results = []
    with open(f"{folder}/{fname}.csv") as f:
        lines =  f.readlines()
        for l in lines:
            results.append(l.strip().split("\t"))
    return results


def _load_alphabet(ab:list):
    res = {}
    last_w = ''
    for a in ab:
        if len(a) == 1:
            last_w = a[0]
        else:
            res[last_w] = a
    return res
def _load_alphabet_all(ab:list):
    res = [] 
    last_w = ''
    for a in ab:
        res.append(
            {"ab_type":a[0],"letter":a[1], "words":a[2:]}
        )
    return res

def get_incorrect_options(ab,words_so_far):
    rnd = random.choices(words_so_far,k=9)
    options = []
    for r in rnd:
        if ab not in r:
            options.append(r)
    return list(set(options))[:6]
    

def save_exercise(folder,ab,ab_type,title,description,correct,options,fname="ab_exercise"):
    with open(f'{folder}/{fname}.csv',"a+") as f:
        f.write(f"{ab_type}\t{ab}\t{title}\t{description}\t{correct}\t{"\t".join(options)}\n")


def gen_exercise(folder, ab_type,ab,words_with_ab,words_so_far,fname="ab_exercise" ):
    description = f"please select words with the letter {ab}"
    title = f"{ab_type} letter {ab}"
    for w in words_with_ab:
        options = get_incorrect_options(ab,words_so_far)
        save_exercise(folder,ab,ab_type,title,description,w,options, fname)

           
def get_words_so_far_for_exercise(folder):
    alphabets = _load_elements(folder, "alphabet")
    words_so_far = ['おはよう','こんにちは','さようなら','話し','気','そう','メアリー','来る','かけ','会っ'] # some words to start with
    for a in alphabets:
        if len(a) ==1:
            words_so_far.append(a[0])
        else:
            ab_type = a[0]
            ab = a[1]
            words_with_ab = a[2:]
            gen_exercise(folder, ab_type,ab,words_with_ab,words_so_far)
        if len(words_so_far) >32:
            words_so_far = words_so_far[10:]
    

def get_extended(folder):
    alphabets = _load_elements(folder, "alphabet_all")
    katakana = {}
    hiragana = {} 
    kanji = {}
    kanji_words = []
    katakana_words = []
    hiragana_words = []
    for a in alphabets:
        ab_type = a[0]
        if ab_type == 'hiragana':
            hiragana[a[1]]=a[2:]
            hiragana_words+=a[2:]
        elif ab_type == 'katakana':
            katakana[a[1]]=a[2:]
            katakana_words +=a[2:]
        elif ab_type == 'kanji':
            kanji[a[1]]=a[2:]
            kanji_words+=a[2:]
    hiragana_words = list(set(hiragana_words))
    katakana_words = list(set(katakana_words))
    kanji_words = list(set(kanji_words))

    for ab,words_with_ab in hiragana.items():
        gen_exercise(folder, 'hiragana',ab,words_with_ab,hiragana_words, fname="ab_all")
    for ab,words_with_ab in katakana.items():
        gen_exercise(folder, 'katakana',ab,words_with_ab,katakana_words, fname="ab_all")
    for ab,words_with_ab in kanji.items():
        gen_exercise(folder, 'kanji',ab,words_with_ab,kanji_words, fname="ab_all")
        
    
async def replace_ab_exercises(lang,to_lang, _id, lesson_id, course_id, module_id, ab_type, ab,alphabets):
    quizes = []
    for a in alphabets:
        if a[0] == ab_type and a[1] == ab:
            quizes.append(a)
    insert_sql = """
    insert into course.exercise(lang,to_lang,course_id, module_id,lesson_id,exercise_type,sentence, options) values (%s,%s,%s,%s,%s,%s,%s,%s)    
    """
    for q in quizes:
        params = (lang,to_lang,course_id, module_id,lesson_id,"alphabet",q[3],q[4:])
        print(insert_sql,params)
        await run_query(insert_sql, params)

    delete_sql = """
    delete from course.exercise where id = %s
    """
    print(delete_sql, (_id,))
    await run_query(delete_sql, (_id,))






async def gen_alphabet_exercise(folder, lang,to_lang):
    sql = """
    SELECT id,lesson_id,course_id, module_id, extra_data from course.exercise 
    where lang = %s and to_lang = %s and exercise_type = 'alphabet'
    """
    res = await get_query_results(sql, (lang, to_lang))
    alphabets = _load_elements(folder, 'ab_exercise')
    # for a in alphabets:
    #     print(a)
    for r in res:
        _id = r.get("id")
        lesson_id = r.get("lesson_id")
        course_id = r.get("course_id")
        module_id = r.get("module_id")
        extra_data = r.get("extra_data")
        ab_type = extra_data[1]
        ab = extra_data[2]
        # print(extra_data)
        await replace_ab_exercises(lang,to_lang,_id,lesson_id,course_id,module_id,ab_type,ab,alphabets)
        


async def fix_alphabet_exercise(lang,to_lang):
    sql = """
    SELECT * from course.exercise 
    where lang = %s and to_lang = %s and exercise_type = 'alphabet'
    """
    res = await get_query_results(sql, (lang, to_lang))
    update_sql = """
    update course.exercise 
    set options = %s,
    to_sentence = %s
    where id = %s
    """
    
    for r in res:
        _id = r.get("id")
        options = r.get("options")
        await run_query(update_sql, (options[1:],options[0], _id))


