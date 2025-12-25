from utils.db import get_query_results
from pydantic import BaseModel
from models.word_select import WordSelect, ModuleWords, WordSelectRequest






async def _get_words_pos(lang: str)-> list[WordSelect]:
    sql = f"""
    select '{lang}' as lang, word, pos, min(min_wcount) as min_wcount, min(max_wcount) as max_wcount ,sum(root_count) as root_count, sum(sentences_count) as sentences_count
    from (
    select word,pos,1 as min_wcount, 3 as max_wcount , sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = '{lang}' and wcount >=2 and wcount <=3 and sentences_count > 5
    group by 1,2
    union all
    select word,pos,4 as min_wcount, 5 as max_wcount ,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = '{lang}' and wcount >=4 and wcount <=5 and sentences_count > 5
    group by 1,2
    union all
    select word,pos,6 as min_wcount, 7 as max_wcount ,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = '{lang}' and wcount >=6 and wcount <=7 and sentences_count > 5
    group by 1,2
    union all
    select word,pos ,8 as min_wcount, 9 as max_wcount ,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = '{lang}' and wcount >=8 and wcount <=10 and sentences_count > 5
    group by 1,2
    union all
    select word,pos,10 as min_wcount, 20 as max_wcount,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = '{lang}' and wcount >=10 and wcount <= 20  and sentences_count > 5
    group by 1,2
    )
    group by 1,2,3
    order by max_wcount, root_count desc, sentences_count desc
    """
    results = await  get_query_results (sql, None)
    words = []
    for r in results:
        words.append(WordSelect(**r))
    return words



async def select_module_words(req:WordSelectRequest) ->list[ModuleWords]:
    """Select words for a module based on the template"""
    all_words = await _get_words_pos(req.lang)
    modules = []
    modules = []
    for i in range(1000):
        if len(all_words) == 0 :
            break
        word_count = int(round(req.words_per_modules + i*req.ratio_increase))
        m = ModuleWords(
            name = f'module {i}',
            num = i,
            words = all_words[:word_count],
            word_count = word_count
        )
        all_words = all_words[word_count:]
        modules.append(m)
    return modules


POS_EN =[
'verb',
'noun',
'adj',
'pron',
'adv',
'intj',
'aux',
'adp',
'sconj',
'det',
'cconj',
'part',
]

POS_JA =[
'verb',
'noun',
'adverb',
'adjective',
'compounds',
]

    
