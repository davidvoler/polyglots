from typing import LiteralString


from utils.db import run_query, get_query_results

kanji_letters = {}
hiragana_letters = {}
katakana_letters = {}


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



async def handle_word(r:dict):
    kanji_l = []
    hiragana_l = []
    katakana_l = []
    w = r.get('word','')
    for c in w:
        if is_kanji(c):
            if c not in kanji_letters:
                kanji_letters[c] = 1
            else:
                kanji_letters[c]+=1
            kanji_l.append(c)
        elif is_hiragana(c):
            if c not in hiragana_letters:
                hiragana_letters[c] = 1
            else:
                hiragana_letters[c]+=1 
            hiragana_l.append(c)
        elif is_katakana(c):
            if c not in katakana_letters:
                katakana_letters[c] = 1
            else:
                katakana_letters[c]+=1
            katakana_l.append(c)
    sql = """
    INSERT INTO content_raw.alphabet_words
    (lang, word,pos,root_count, wcount,sentences_count,lemma,rank,
    kanji_count, hiragana_count,katakana_count,
    kanji_letters,hiragana_letters,katakana_letters)
    values(%s,%s,%s,%s,%s, %s,%s,%s,
    %s,%s,%s,
    %s,%s,%s
    )
    """
    await run_query(sql,(
        'ja', w,r.get('pos','') or '', r.get('root_count'),r.get('wcount'),r.get('sentences_count'),r.get('lemma'),r.get('rank'),
        len(kanji_l), len(hiragana_l),len(katakana_l),
        "".join(kanji_l),
        "".join(hiragana_l),
        "".join(katakana_l)
    ))


async def save_letters():
    sql = """
    INSERT INTO content_raw.alphabet 
    (lang, ab_type, letter, words_count)
    VALUES(
    %s,%s,%s,%s
    )
    """
    for k, v in kanji_letters.items():
        await run_query(sql, ('ja','j',k,v ))
    for k, v in hiragana_letters.items():
        await run_query(sql, ('ja','h',k,v ))
    for k, v in katakana_letters.items():
        await run_query(sql, ('ja','k',k,v ))

async def collect_words():
    sql = """
        select lang, word, min(pos) ,sum(root_count) as root_count, min(wcount) as wcount,
        sum(sentences_count) as sentences_count,min(lemma) as lemma,min(rank) as rank
        from content_raw.words_pos1 
        where lang = 'ja'group by 1,2
    """
    results = await get_query_results(sql,None)
    for r in results:
        await handle_word(r)
    await save_letters()

