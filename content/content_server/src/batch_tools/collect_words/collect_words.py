from utils.db import get_query_results, run_query
from collections import OrderedDict
from wordfreq import zipf_frequency
from pydantic import BaseModel 


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
            'w_count1_3': 0,
            'w_count4_5': 0,
            'w_count6_9': 0,
            'w_count10_20': 0,
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
        words[word]['w_count1_3'] += 1
    elif w_count >= 4 and w_count <= 5:
        words[word]['w_count4_5'] += 1
    elif w_count >= 6 and w_count <= 9:
        words[word]['w_count6_9'] += 1
    elif w_count >= 10:
        words[word]['w_count10_20'] += 1




async def _insert_words(words:dict, lang:str):
    sql = """
    insert into content_raw.words (lang, word, root_count, count, lemma, rank, w_count1_3, 
                                   w_count4_5, w_count6_9, w_count10_20, translit1, translit2, 
                                   translit3, meaning,verb, noun, adjective, adverb, 
                                   auxiliary_verb, particle, pronoun, conjunction, compound_pattern)
                                   values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for k,v in words.items():
        print(v.get('types'))
        rank = rank_word(k, lang)
        verb = 'verb' in v.get('types')
        noun = 'noun' in v.get('types')
        adjective = 'adjective' in v.get('types') or 'adj' in v.get('types')
        adverb = 'adverb' in v.get('types') or 'adv' in v.get('types')
        auxiliary_verb = 'auxiliary_verb' in v.get('types') or 'aux' in v.get('types')
        particle = 'particle' in v.get('types') or 'p' in v.get('types')
        pronoun = 'pronoun' in v.get('types') or 'pron' in v.get('types')
        conjunction = 'conjunction' in v.get('types') or 'sconj'  in v.get('types')
        compound_pattern = 'compound_pattern' in v.get('types') or 'cp' in v.get('types')   
        await run_query(sql, (lang, k,v.get('root_count'), v.get('count'), v.get('lemma'), rank, 
        v.get('w_count1_3'), v.get('w_count4_5'), v.get('w_count6_9'), v.get('w_count10_20'), 
        v.get('translit1'), v.get('translit2'), v.get('translit3'), v.get('meaning'),
        verb, noun, adjective, adverb, auxiliary_verb, particle, pronoun, conjunction, compound_pattern))


async def _insert_words_pos(words:dict, lang:str):
    sql = """
    insert into content_raw.words_pos (lang, word, pos, root_count, count, lemma, rank, 
    wc1, wc2, wc3, wc4, wc5, wc6, wc7, wc8, wc9, wc10, wc11, wc12, wc13, wc14, wc15, wc16, wc17_and_more)
    values( %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    on conflict (lang, word, pos) do nothing
    """
    for _,v in words.items():
        params = (lang, v.get('word'), v.get('pos'), v.get('root_count'), v.get('count'), v.get('lemma'), 
        v.get('rank'), 
        v.get('1'), v.get('2'), v.get('3'), v.get('4'), v.get('5'), v.get('6'),
        v.get('7'), v.get('8'), v.get('9'), v.get('10'), v.get('11'), v.get('12'), v.get('13'), 
        v.get('14'), v.get('15'), v.get('16'), v.get('17_and_more'))
        print(len(params))
        await run_query(sql, params)   


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
                wtype = e.get('pos','').lower()
                is_root = e.get('dep') == 'ROOT' 
            meaning = e.get('meaning','')
            lemma = e.get('lemma','')
            _add_word(words, e.get('text'), wtype, lemma, w_count, translit1, translit2, translit3, meaning, is_root)

    await _insert_words(words, lang)



def _add_word_pos(words:list, word:str, lang:str, pos:str,w_count:int, lemma='', is_root:bool=False):
    key = f"{word}_{pos}"
    if key not in words:
        words[key] = {
            'word': word,
            'pos': pos,
            'lemma': lemma,
            'root_count':0,
            '0':0,
            '1':0,
            '2':0,
            '3':0,
            '4':0,
            '5':0,
            '6':0,
            '7':0,
            '8':0,
            '9':0,
            '10':0,
            '11':0,
            '12':0,
            '13':0,
            '14':0,
            '15':0,
            '16':0,
            '17_and_more':0,
            'rank':rank_word(word, lang),
            'count':0,
        }
    if is_root:
        words[key]['root_count'] += 1
    if w_count <= 16:
        words[key][str(w_count)] += 1
    else:
        words[key]['17_and_more'] += 1
    words[key]['count'] += 1

async def collect_words_pos(lang:str):
    results = await _get_elements_data(lang)
    words = {}
    for r in results:
        elements = r.get('elements', [])
        w_count = len(elements)
        root = r.get('root', '')
        for e in elements:
            if lang == 'ja':
                if e.get('text') == root:
                    is_root = True
                else:
                    is_root = False
                pos = e.get('type')
            else:
                is_root = e.get('dep') == 'ROOT'
                pos = e.get('pos','').lower()
            _add_word_pos(words, e.get('text'), lang, pos, w_count, e.get('lemma'), is_root)
    await _insert_words_pos(words, lang)



class Word(BaseModel):
    word:str
    pos:str = ''
    w_count: int = 0
    lemma: str = ''
    rank:int = 0
    sentence_count: int = 0
    root_count: int = 0
    def key(self):
        return f'{self.word}_{self.pos}_{self.w_count}'


async def _insert_words_pos1(words:dict, lang:str):
    sql = """
    insert into content_raw.words_pos1 (lang, word, pos,wcount, root_count, sentences_count, lemma, rank)
    values( %s, %s, %s, %s, %s, %s, %s, %s)
    on conflict (lang, word, pos,wcount) do nothing
    """
    for _,v in words.items():
        params = (lang, v.word, v.pos,v.w_count, v.sentence_count, v.root_count,  v.lemma, v.rank)
        print(len(params))
        await run_query(sql, params)   


async def collect_words_pos1(lang:str):
    results = await _get_elements_data(lang)
    words = {}
    for r in results:
        elements = r.get('elements', [])
        w_count = len(elements)
        root = r.get('root', '')
        for e in elements:
            if lang == 'ja':
                if e.get('text') == root:
                    is_root = True
                else:
                    is_root = False
                pos = e.get('type')
            else:
                is_root = e.get('dep') == 'ROOT'
                pos = e.get('pos','').lower()
            w = Word(word = e.get('text'),pos=pos, lemma=e.get("lemma",''), w_count = w_count)
            if w.key() not in words:
                w.rank = rank_word(w.word, lang)
                words[w.key()] = w 
            words[w.key()].sentence_count +=1
            if is_root:
                words[w.key()].root_count +=1
    await _insert_words_pos1(words, lang)




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
    conjunction bool default false,
    compound_pattern bool default false,
    particle bool default false,
    pronoun bool default false,
    interjection bool default false,
    primary key (lang, word)
);
"""
