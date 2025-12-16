from pydantic import BaseModel


class ByWordsRequest(BaseModel):
    lang: str
    words_count: int = -1
    word_type: str = 'word' # word, root_lemma, adverb, verb, noun, adjective, auxiliary_verb
    limit: int = 200
    offset: int = 0


class WordCount(BaseModel):
    word: str
    cnt: int

class ByWordResponse(BaseModel):
    lang: str
    words_count: int = -1
    word_type: str = 'word' # word, root_lemma, adverb, verb, noun, adjective, auxiliary_verb
    words: list[WordCount]
    limit: int = 200
    offset: int = 0
    