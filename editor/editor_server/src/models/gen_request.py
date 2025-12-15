from pydantic import BaseModel


class GenByWordsRequest(BaseModel):
    lang: int
    words_count: int = 3
    by_root_lemma: bool = False
    by_word: bool = False
    by_frequency: bool = False
