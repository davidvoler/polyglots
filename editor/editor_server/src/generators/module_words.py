from utils.db import get_query_results
from pydantic import BaseModel

from generators.course_template import CourseTemplate

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


class WordSelect(BaseModel):
    lang: str
    pos: str
    max_wcount: int
    min_wcount: int
    sentences_count: int
    is_root: bool = False
    def key(self):
        return f"{self.lang}-{self.pos}"


sentences_len_groups = [ 
    (1, 3),
    (4, 5),
    (6, 7),
    (8, 10),
    (11, 16),
    (17, 20),
]

async def _get_words_pos(lang: str,  max_wcount: int, min_wcount: int, pos: str=''):
    sql = """
    select word, pos, min(grp) as grp,sum(root_count) as root_count, sum(sentences_count) as sentences_count
    from (
    select word,pos,1 as grp, sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = 'ja' and wcount >=1 and wcount <=3 and sentences_count > 5
    group by 1,2
    union all
    select word,pos,2 as grp,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = 'ja' and wcount >=4 and wcount <=5 and sentences_count > 5
    group by 1,2
    union all
    select word,pos,3 as grp,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = 'ja' and wcount >=6 and wcount <=7 and sentences_count > 5
    group by 1,2
    union all
    select word,pos as grp,4,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = 'ja' and wcount >=8 and wcount <=10 and sentences_count > 5
    group by 1,2
    union all
    select word,pos,5 as grp,sum(root_count) as  root_count, sum(sentences_count) as sentences_count from content_raw.words_pos1 
    where lang = 'ja' and wcount >10  and sentences_count > 5
    group by 1,2
    )
    group by 1,2 
    order by grp, root_count desc, sentences_count desc
    """

async def _get_roots(lang: str,  max_wcount: int, min_wcount: int, pos: str=''):
    pass


async def get_all_words_by_sentences_len(template: CourseTemplate):
    """Select words for a module based on the template"""
    all_words = {f"{len_group[0]}-{len_group[1]}": {} for len_group in sentences_len_groups}
    
    for len_group in sentences_len_groups:
        words_root = await _get_roots(template.lang, len_group[0], len_group[1])
        for w in words_root:
            all_words[f"{len_group[0]}-{len_group[1]}"][w.key()] = w
        words = await _get_words_pos(template.lang, len_group[0], len_group[1])
        for w in words:
            if w.key() not in all_words[f"{len_group[0]}-{len_group[1]}"]:
                all_words[f"{len_group[0]}-{len_group[1]}"][w.key()] = w

    return all_words


"""

TODO:
order the words in some logic
create module 
-assgin words to module 
return a list of module 



"""

