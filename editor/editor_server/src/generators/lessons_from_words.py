from utils.db import get_query_results
from models.word_select import WordSelect
from models.gen_course import Question, Lesson,Module


WORDS_SO_FAR = set[str]()
WORD_SO_FAR_IN_SENTENCES = set[str]()
KANJI_SO_FAR = set[str]()
HIRAGANA_SO_FAR = set[str]()
KATAKANA_SO_FAR = set[str]()
IDS_SO_FAR = set[int]()

def create_lesson(word, idx):
    # TODO: load sentences translation and options with the word in them 
    return {}

def create_greeting_lessons():
    return {}

def create_descriptions_lessons(descriptions):
    return {}

def create_greeting_lesson():
    return {}


async def create_question(word, lang:str, to_lang:str)->Question:
    sql = """
    SELECT l.id as id, l.lang as lang, l.text as sentence,t.text as translation,
    t.lang as to_lang, t.options as options
    from content_raw.sentence_elements l 
    join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
    join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
    where tl.lang = %s and tl.to_lang = %s and (l.root = %s or l.word1 = %s or l.word2 = %s or l.word3=%s)
    order by l.len_elm limit 30
    """
    # print(sql)
    results = await get_query_results(sql, (lang, to_lang, word, word,word,word))
    questions = []
    for r in results:
        q = Question(**r)
        questions.append(q)
    return questions
 

async def create_greeting_lessons(fpath, lang:str, to_lang:str)->Question:
    from generators.ja.greeting import GREETING_WORDS
    questions = []

    for gr in GREETING_WORDS:
        sql = f"""
        SELECT l.id as id, l.lang as lang, l.text as sentence,t.text as translation,
        t.lang as to_lang, t.options as options
        from content_raw.sentence_elements l 
        join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
        join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
        where tl.lang = %s and tl.to_lang = %s and l.text like %s
        order by l.len_elm limit 30
        """
        # print(sql)
        results = await get_query_results(sql, (lang, to_lang, f'%{gr}%'))
        for r in results:
            q = Question(**r)
            q.word = gr
            q.question_type = 'greetings'
            questions.append(q)
            with open(f'{fpath}/greeting_q.csv', "a+") as f:
                options_str = "\t".join(q.options)
                f.write(f"{q.word}\t{q.id}\t{q.lang}\t{q.to_lang}\t{q.sentence}\t{q.translation}\t{options_str}\n")
    return questions



async def load_words(path, course_path, lang,to_lang):
    print(lang,to_lang)
    words = []
    with open(path) as f:
        lines = f.readlines()
        for l in lines:
            f = l.split('\t')
            w = WordSelect(
                    lang = f[0],
                    word = f[1],
                    pos = f[2],
                    min_wcount = f[3],
                    max_wcount = f[4],
                    sentences_count = f[5],
                    root_count= f[6])
            words.append(w)
    print(len(words))
    lessons = []
    i = 0
    for w in words:
        i+=1
        questions = await create_question(w.word, lang, to_lang)
        with open(course_path, "+a") as f:
            for q in questions:
                options_str = "\t".join(q.options)
                f.write(f"{w.word}\t{q.id}\t{w.lang}\t{q.to_lang}\t{q.sentence}\t{q.translation}\t{options_str}\n")
    return lessons
    
        

