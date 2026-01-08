from utils.db import get_query_results
import json

WORDS_SO_FAR = set[str]()
WORDS_IN_SENTENCE = set[str]()
HIRAGANA_SO_FAR = set[str]()
KATAKANA_SO_FAR = set[str]()
KANJI_SO_FAR = set[str]()



async def create_course(lang, to_lang, title, description):
    sql = """
    INSERT INTO content.course(lang,to_lang,title,description) VALUES (%s, %s, %s,%s) RETURNING id
    """
    params = (lang, to_lang, title, description)
    res = await get_query_results(sql, params)
    return res[0].get('id')

async def create_module(lang, to_lang, title, description, course_id):
    sql = """
    INSERT INTO content.module(lang,to_lang,title,description, course_id) VALUES (%s, %s, %s,%s,%s) RETURNING id
    """
    params = (lang, to_lang, title, description,course_id )
    res = await get_query_results(sql, params)
    return res[0].get('id')

async def create_lesson(lang, to_lang, title, description, course_id, module_id):
    sql = """
    INSERT INTO content.lesson(lang,to_lang,title,description, course_id, module_id) VALUES (%s, %s, %s,%s,%s,%s) RETURNING id
    """
    params = (lang, to_lang, title, description,course_id, module_id )
    res = await get_query_results(sql, params)
    return res[0].get('id')

async def create_exercise(lang, to_lang, course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type="sentence",extra_data=[]):
    sql = """
    INSERT INTO content.exercise(lang,to_lang,course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type,extra_data) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """
    params = (lang, to_lang,course_id, module_id,lesson_id, sentence_id, to_sentence_id,exercise_type,json.dumps(extra_data))
    await get_query_results(sql, params)
    
async def create_ab_exercise(lang, to_lang, course_id, module_id,lesson_id, sentence, to_sentence,options):
    sql = """
    INSERT INTO content.exercise(lang,to_lang,course_id, module_id,lesson_id, sentence, to_sentence,exercise_type, options) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """
    params = (lang, to_lang,course_id, module_id,lesson_id, sentence, to_sentence,'alphabet',options)
    await get_query_results(sql, params)


def _load_elements(folder, fname):
    res = []
    with open(f"{folder}/{fname}.csv") as f:
        for l in f.readlines():
            res.append(l.strip().split("\t"))
    return res



async def create_course_from_file(path,lang, to_lang, title, description):
    elements = _load_elements(path, "modules")
    course_id = await create_course(lang, to_lang, title, description)
    module_id = 0
    lesson_id = 0
    for e in elements:
        l = e.split("\t")
        if l[0] == "M":
            title = e.replace("M\t","").replace("\t",", ").replace("|","").strip().replace("by_words","words")
            module_id = await create_module(lang, to_lang, title, title, course_id)
        elif l[0] == "L":
            title = e.replace("L\t","").replace("by_words","").strip()
            lesson_id = await create_lesson(lang, to_lang, title, title, course_id,module_id)
        elif l[0] == "S":
            if l[1] in ["kanji","katakana",'hiragana']:
                await create_exercise(lang, to_lang,course_id, module_id,lesson_id, 0, 0 ,"alphabet",l)
            else:
               await create_exercise(lang, to_lang,course_id, module_id,lesson_id, l[2], l[5])






async def load_all_alphabet_exercises(folder, lang, to_lang):
    course_id = 30
    hiragana = []
    katakana = []
    kanji = []
    all_alphabet = _load_elements(folder, 'ab_all')
    for a in all_alphabet:
        print(a)
    for a in all_alphabet:
        if a[0] == 'hiragana':
            hiragana.append(a)
        elif a[0] == 'katakana':
            katakana.append(a)
        elif a[0] == 'kanji':
            kanji.append(a)
    module_id = await create_module(lang, to_lang, 'Hiragana', 'Hiragana', course_id)
    hiragana_letters = {}
    for a in hiragana:
        if a[1] in hiragana_letters:
            hiragana_letters[a[1]]+=1
        else:
            hiragana_letters[a[1]] = 1
            title = f"Hiragana {a[1]}"
            lesson_id = await create_lesson(lang, to_lang, title, title, course_id, module_id)
        await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, a[3],a[4], a[5:] )
    module_id = await create_module(lang, to_lang, 'Kanji', 'Kanji', course_id)
    kanji_letters = {}
    for a in kanji:
        if a[1] in kanji_letters:
            kanji_letters[a[1]]+=1
        else:
            kanji_letters[a[1]] = 1
            title = f"Kanji {a[1]}"
            lesson_id = await create_lesson(lang, to_lang, title, title, course_id, module_id)
        await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, a[3],a[4], a[5:] )
    module_id = await create_module(lang, to_lang, 'katakana', 'katakana', course_id)
    katakana_letters = {}
    for a in katakana:
        if a[1] in katakana_letters:
            katakana_letters[a[1]]+=1
        else:
            katakana_letters[a[1]] = 1
            title = f"Katakana {a[1]}"
            lesson_id = await create_lesson(lang, to_lang, title, title, course_id, module_id)
        await create_ab_exercise(lang, to_lang,course_id, module_id,lesson_id, a[3],a[4], a[5:])

async def letter_in_words_single_choice(exercise: dict) -> int:
    # we already have that one
    pass
async def letter_in_words_multiple_choice(exercise: dict) -> int:
    # get extra words with the letter in them
    # create the new exercise with extra words    
    pass 
async def words_in_sentence_multiple_choice(exercise: dict) -> int:
    pass 
async def words_in_sentence_multiple_choice(exercise: dict) -> int:
    pass 
async def words_in_array(exercise: dict) -> int:
    pass 
async def memory_game_letters(exercise: dict) -> int:
    pass 
async def memory_game_words(exercise: dict) -> int:
    pass 
async def type_words(exercise: dict,ab_type: str, extra_letters: str= "") -> int:
    pass  


async def create_alphabet_exercises(ab_type, ab_letter):
    if ab_type == 'hiragana':
        HIRAGANA_SO_FAR.add(ab_letter)
        memory_game_letters(ab_letter,HIRAGANA_SO_FAR)
    elif ab_type == 'katakana':
        KATAKANA_SO_FAR.add(ab_letter)
    elif ab_type == 'kanji':
        KANJI_SO_FAR.add(ab_letter)
    

async def create_sentence_exercises(m, word):
    pass

async def handle_module(m):
    pass

async def handle_lesson(m):
    pass

    

async def gen_from_modules(folder, lang, to_lang):
    modules = _load_elements(folder, "modules")
    last_lesson_type = ''
    last_lesson_word = ''
    ab_type = ''
    ab_letter = ''
    for m in modules:
        if m[0] == "M":
            await handle_module(m)
        elif m[0] == "L":
            last_lesson_type = m[1]
            if last_lesson_type == 'alphabet':
                ab_type = m[2]
                ab_letter = m[3]
            else:
                last_lesson_word = m[2]
        elif m[0] == "S":
            if m[1] in ["kanji","katakana",'hiragana']:
                await create_alphabet_exercises(ab_type, ab_letter, words)
            else:
                await create_sentence_exercises(last_lesson_word)
            
            


