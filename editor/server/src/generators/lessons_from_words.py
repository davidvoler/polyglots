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
    SELECT l.id as id, l.lang as lang, l.text as sentence,t.text as translation,t.id as to_id,
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
 

async def create_question_no_duplicates(word, lang:str, to_lang:str)->Question:
    sql = """
    SELECT l.id as id, l.lang as lang, l.text,t.lang as to_lang, min(t.id) as to_id
    from content_raw.sentence_elements l 
    join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
    join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
    where tl.lang = %s and tl.to_lang = %s and (l.root = %s or l.word1 = %s or l.word2 = %s or l.word3=%s)
    group by 1,2,3,4
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
        SELECT l.id as id, l.lang as lang, l.text as sentence, first(t.text) as translation,first(t.id) as to_id,
        t.lang as to_lang, t.options as options
        from content_raw.sentence_elements l 
        join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
        join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
        where tl.lang = %s and tl.to_lang = %s and l.text like %s
        group by 1,2,3
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



async def load_words_no_duplicate(path, course_path, lang,to_lang):
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
        questions = await create_question_no_duplicates(w.word, lang, to_lang)
        with open(course_path, "+a") as f:
            for q in questions:
                f.write(f"{w.word}\t{q.id}\t{w.lang}\t{q.to_lang}\t{q.to_id}\t{q.sentence}\n")
    return lessons

# def add_so_far(word:str):
#     WORDS_SO_FAR.add():
#     for c in word:
        




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
    
        




def is_hiragana(char):
    """Check if a character is Hiragana"""
    return '\u3040' <= char <= '\u309F'

def is_katakana(char):
    """Check if a character is Katakana"""
    return ('\u30A0' <= char <= '\u30FF') or ('\u31F0' <= char <= '\u31FF')

def is_kanji(char):
    """Check if a character is Kanji"""
    return ('\u4E00' <= char <= '\u9FAF') or \
           ('\u3400' <= char <= '\u4DBF') or \
           ('\uF900' <= char <= '\uFAFF')


async def alphabet_by_words(path, course_path, lang,to_lang):
    hiragana = {}
    katakana = {}
    kanji = {}
    learned = set[str]()    
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
    
    
    for word in words:
        w = word.word
        lessons = []
        for c in w:
            if is_hiragana(c):
                if c not in hiragana:
                    hiragana[c] = set([w])
                else:
                    hiragana[c].add(w)
            elif is_kanji(c):
                if c not in kanji:
                    kanji[c] = set([w])
                else:
                    kanji[c].add(w)
            elif is_katakana(c):
                if c not in katakana:
                    katakana[c] = set([w])
                else:
                    katakana[c].add(w)
        for j,val in kanji.items():
            if j in learned:
                continue
            if len(val) >= 3:
                lessons.append(('kanji',j,list(val)))
                learned.add(j)
        for j,val in hiragana.items():
            if j in learned:
                continue
            if len(val) >= 3:
                lessons.append(('hiragana',j,list(val)))
                learned.add(j)
        for j,val in katakana.items():
            if j in learned:
                continue
            if len(val) >= 3:
                lessons.append(('katakana',j,list(val)))
                learned.add(j)
        with open(course_path, 'a+') as f:
            f.write(w + "\n")
            for l in lessons:
                l_words = '\t'.join(l[2])
                f.write(f"{l[0]}\t{l[1]}\t{l_words}\n")
        
        
    lessons = []
    for j,val in kanji.items():
        lessons.append(('kanji',j,list(val)))
    for j,val in hiragana.items():
        lessons.append(('hiragana',j,list(val)))
    for j,val in katakana.items():
        lessons.append(('katakana',j,list(val)))
    with open(course_path, 'a+') as f:
        for l in lessons:
            l_words = '\t'.join(l[2])
            f.write(f"{l[0]}\t{l[1]}\t{l_words}\n")

async def gen_description_lessons(target_path):
    from generators.ja.descriptions import DESCRIPTIONS
    
    with open(target_path, 'w') as f:
        for d in DESCRIPTIONS:
            f.write("\t".join(d) +"\n")
        

async def collect_course(source_folder):
    #load greetings
    # load words
    # load alphabet 
    
    # load descriptions 

    """write course in the following order
    1. greeting - module
    2. load words - 
    3. start with 2 lessons per word
    4. add description every 10 lessons until we have no more descriptions 
    5. after 40 lessons switch to lesson per word 
    6. add alphabet 
    """
    pass 
    

