from collections import OrderedDict
from wordfreq import zipf_frequency


def get_ranked_words(words:list,lang, max_rank=910, min_rank=260, words_count=3):
    ranked = {}
    words = list(set(words))
    if len (words) == 1:
        return words
    for w in words:
        r = 1000 - int(zipf_frequency(w,lang) * 100)
        if r <= max_rank and r> min_rank:
            if r not in ranked:
                ranked[r] = [w]
            else:
                ranked[r].append(w)
        else:
            print(f"word {w} is not ranked {r}")
    sorted_by_rank = OrderedDict(sorted(ranked.items()))
    words  = list(sorted_by_rank.values())[::-1]
    results = []
    for w in words:
        results = results + w
    return results[:words_count]

if __name__ == "__main__":
    words = ["大きい", "文明", "築い", "けれども", "表記", "法", "なかっ"]
    lang = "ja"
    print(get_ranked_words(words, lang, words_count=4))