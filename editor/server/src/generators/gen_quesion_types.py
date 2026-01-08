from utils.db import get_query_results, run_query

ALL_HIRAGANA_LETTERS = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
ALL_KATAKANA_LETTERS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
SOME_KANJI_LETTERS = """人千日番乗塁百立向抜野子方笑道名世口銭出玉色釣捜探余金中坊歩師合墨回悲所飯早頃者石薬卵寝伏"""



async def add_weight(sentence: str) -> int:
    sql = """select * from course.exercise
    order by lesson_id, module_id, course_id
    """
    results = await get_query_results(sql)

async def multiple_choice_sentence(exercise: dict) -> int:
    sentence_id = exercise.get('id') 
    lang = exercise.get('lang')
    to_lang = exercise.get('to_lang')
    sql = """
    SELECT l.id as id, l.lang as lang, l.text,t.lang as to_lang, min(t.id) as to_id
    from content_raw.sentence_elements l 
    join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
    join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
    where tl.lang = %s and tl.to_lang = %s 
    and l.id = %s
    """
    results = await get_query_results(sql, (lang, to_lang, sentence_id))
    if len(results) >1:
        pass
    return None

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



async def load_exercises(lang: str, to_lang: str,course_id: int) -> list[dict]:
    sql = """
    SELECT id,lesson_id,course_id, module_id, extra_data from course.exercise 
    where lang = %s and to_lang = %s and course_id = %s and exercise_type = 'alphabet'
    order by module_id, lesson_id
    """
    results = await get_query_results(sql, (lang, to_lang))
    for r in results:
        _id = r.get("id")
        lesson_id = r.get("lesson_id")
        course_id = r.get("course_id")
        module_id = r.get("module_id")
        sentence = r.get("sentence")
        options = r.get("options")
        to_sentence = r.get("to_sentence")
        letter = sentence[-1]
        print(sentence, options, to_sentence, letter)
        
