from binascii import Incomplete
from utils.db import get_query_results, run_query
import random

AUXILIARY_VERBS = set()
ALL_HIRAGANA_LETTERS = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
ALL_KATAKANA_LETTERS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
SOME_KANJI_LETTERS = """人千日番乗塁百立向抜野子方笑道名世口銭出玉色釣捜探余金中坊歩師合墨回悲所飯早頃者石薬卵寝伏"""


async def extract_aux():
    sql = """
    SELECT elements from content_raw.sentence_elements 
    where lang = 'ja'
    """
    results = await get_query_results(sql, None)
    for r in results:
        elements = r.get("elements")
        for e in elements:
            if e.get("type") == "verb":
                aux = e.get("auxiliary_verb")
                if aux:
                    AUXILIARY_VERBS.add(aux)
    for aux in AUXILIARY_VERBS:
        print(aux)

async def load_words():
    words = set()
    sql = """
    SELECT word from content_raw.words_pos1 
    where lang = 'ja'
    group by 1
    """
    results = await get_query_results(sql, None)
    for r in results:
        w = r.get("word")
        words.add(w)
    return list(words)

async def identify_words(sentences_id: int):
    all_words = await load_words()
    sql = """
    SELECT * from content_raw.sentence_elements 
    where lang = 'ja' and id = %s
    """
    results = await get_query_results(sql, (sentences_id,))
    for r in results:
        words = r.get("words")
        text = r.get("text")
        correct = words
        r = random.choices(all_words, k=4)
        incorrect = [w for w in r if w not in text]
    print(correct, incorrect, text)
    return correct, incorrect

async def letter_in_words():
    all_words = await load_words()
    hiragana_letters = list(ALL_HIRAGANA_LETTERS)
    for l in hiragana_letters:
        correct = []
        incorrect = []
        random.shuffle(all_words)
        for w in all_words:
            if l in w:
                correct.append(w)
            else:
                if len(incorrect) < 4:
                    incorrect.append(w)
            if len(correct) >= 3 and len(incorrect) >= 3:
                break
        print(l,correct, incorrect)

async def memory_game_letters():
    hiragana_letters = list(ALL_HIRAGANA_LETTERS)
    hiragana_letters1 = list(ALL_HIRAGANA_LETTERS)
    
    for l in hiragana_letters:
        correct = []
        incorrect = []
        for w in all_words:
            if l in w:
                correct.append(w)
            else:
                if len(incorrect) < 4:
                    incorrect.append(w)
        print(l,correct, incorrect)

