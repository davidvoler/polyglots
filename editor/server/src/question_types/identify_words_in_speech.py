import random

async def identify_words_in_speech(
    words:list, 
    text:str, 
    word_collections:list
):
    rnd = random.choices(word_collections, k=6)
    incorrect = []
    for ic in rnd:
        if ic not in text:
            incorrect.append(ic)
    return words,text,incorrect

