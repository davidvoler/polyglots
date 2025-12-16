from utils.db import get_query_results, run_query
from collections import OrderedDict
from wordfreq import zipf_frequency

def rank_word(word:str,lang):
    return  1000 - int(zipf_frequency(word,lang) * 100)



WORDS_TO_EXCLUDE = ["'nt", 'it', 'the']

async def _get_elements_data(lang:str):
    sql = """
    select id, text, elements,root,root_lemma from content_raw.sentence_elements
    where lang = %s
    """
    results = await get_query_results(sql, (lang,))
    return results

    
def _add_word(words, word, wtype, lemma='',
             w_count=0, translit1='', translit2='', translit3='',
             meaning='', is_root:bool=False):
    if word not in words:
        words[word] = {
            'types': set(),
            'count': 0,
            'lemma': lemma,
            'w_count1-3': 0,
            'w_count4-5': 0,
            'w_count6-9': 0,
            'w_count10-20': 0,
            'root_count': 0,
            'translit1': translit1,
            'translit2': translit2,
            'translit3': translit3,
            'meaning': meaning,
            'rank': 0,
        }
    words[word]['types'].add(wtype)
    words[word]['count'] += 1
    if is_root:
        words[word]['root_count'] += 1
    if w_count >= 1 and w_count <= 3:
        words[word]['w_count1-3'] += 1
    elif w_count >= 4 and w_count <= 5:
        words[word]['w_count4-5'] += 1
    elif w_count >= 6 and w_count <= 9:
        words[word]['w_count6-9'] += 1
    elif w_count >= 10 and w_count <= 20:
        words[word]['w_count10-20'] += 1




async def _insert_words(words:dict, lang:str):
    sql = """
    insert into content_raw.words (lang, word, root_count, count, lemma, rank, w_count1_3, 
                                   w_count4_5, w_count6_9, w_count10_20, translit1, translit2, 
                                   translit3, meaning, types, verb, noun, adjective, adverb, 
                                   auxiliary_verb)
                                   values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for k,v in words.items():
        rank = rank_word(w, lang)
        wtypes = ', '.join(v.get('types'))
        await run_query(sql, (lang, k,v.get('root_count'), v.get('count'), v.get('lemma'), rank, v.get('w_count1_3'), v.get('w_count4_5'), v.get('w_count6_9'), v.get('w_count10_20'), v.get('translit1'), v.get('translit2'), v.get('translit3'), v.get('meaning'), v.get('types'), v.get('verb'), v.get('noun'), v.get('adjective'), v.get('adverb'), v.get('auxiliary_verb')))


async def collect_words(lang:str):
    results = await _get_elements_data(lang)
    words = {}
    for r in results:
        elements = r.get('elements', [])
        root = r.get('root', '')
        root_lemma = r.get('root_lemma', '')
        w_count = len(elements)
        _add_word(words, root, 'root', root_lemma, w_count)
        for e in elements:
            if lang == 'ja':
                translit1 = e.get('roma')
                translit2 = e.get('hira')
                translit3 = e.get('kana')
                wtype = e.get('category')
                is_root = e.get('lemma') == root_lemma and e.get('text') == root
            else:
                translit1 = ''
                translit2 = ''
                translit3 = ''
                wtype = e.get('pose')
                is_root = e.get('dep') == 'ROOT' 
            meaning = e.get('meaning','')
            lemma = e.get('lemma','')
            _add_word(words, e.get('text'), wtype, lemma, w_count, translit1, translit2, translit3, meaning, is_root)

    await _insert_words(words, lang)

"""
[{"hira": "おちつけ", "kana": "オチツケ", "roma": "ochitsuke", "text": "落ち着け", "type": "verb", "lemma": "落ち着く", "meaning": "", "category": "verb", "position": 0}]
[{"dep": "det", "pos": "DET", "text": "the", "lemma": "the"}, {"dep": "nsubj", "pos": "NOUN", "text": "dogs", "lemma": "dog"}, {"dep": "ROOT", "pos": "VERB", "text": "followed", "lemma": "follow"}]

CREATE TABLE content_raw.words (
    lang varchar(12) not null,
    word varchar(100) not null,
    root_count int default 0,
    count int default 0,
    lemma varchar(100) not null,
    rank int2 default 0,
    w_count1_3 int default 0,
    w_count4_5 int default 0,
    w_count6_9 int default 0,
    w_count10_20 int default 0,
    translit1 varchar(100) default '',
    translit2 varchar(100) default '',
    translit3 varchar(100) default '',
    meaning varchar(100) default '',
    adverb bool default false,
	verb bool default false,
	auxiliary_verb bool default false,
	noun bool default false,
	adjective bool default false,
    primary key (lang, word)
);
"""
