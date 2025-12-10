

def analyze_sentence(text:str, id:int) -> dict:
    return {
        "text": text,
        "id": id,
        "elements": [],
        "kanji_count": 0,
        "hiragana_count": 0,
        "katakana_count": 0,
        "other_count": 0
    }
