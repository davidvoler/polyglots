from wordfreq import zipf_frequency

def rank_words(lang, word) -> int:
    r = 1000 - int(zipf_frequency(word,lang) * 100)
    # return r, zipf_frequency(word,lang)
    return r


if __name__ == "__main__":
    words = ["hello", "world", "python", "code", "programming", "it", "apple", "banana", "orange", "grape", "the", "a", "an", "and", "is", "to", "in", "of", "for", "on", "with", "as", "by", "at", "this", "that", "which", "who", "whom"]
    for w in words:
        print(f"Word: {w}, Rank: {rank_words('en', w)}")




