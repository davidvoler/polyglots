

kanji_words = set()
hiragana_words = set()
katakana_words = set()

kanji_letters = ={}
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





async def handle_word():
    kanji_letters = []
    hiragana_letters = []
    katkkana_leters = []
    for c in words:
        if is_kanji(c):
            kanji_letters

def handle_word(w):
    kanji_count = 0
    for c in w:
        if is_hiragana(c):
            if c not in hiragana_letters:
                hiragana_letters[c] = set([w])
            else:
                hiragana_letters[c].add(w)
            hiragana_words.add(w)
        if is_katakana(c):
            if c not in katakana_letters:
                katakana_letters[c] = set([w])
            else:
                katakana_letters[c].add(w)
            hiragana_words.add(w)
        if is_kanji(c)
            if c not in kanji_letters:
                kanji_letters[c] = set([w])
            else:
                kanji_letters[c].add(w)
            kanji_words.add(w)

        


    


