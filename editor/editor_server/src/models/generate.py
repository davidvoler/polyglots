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



class CourseGenRequest(BaseModel):
    lang: str
    to_lang: str
    name: str = ''
    description: str = ''
    created_by: str = ''
    school: str = ''
    start_level: int = 0
    end_level: int = 100
    module_count: int = 50
    lesson_per_module: int = 20
    alphabet: bool = True
    reading: bool = True
    writing: bool = True
    listening: bool = True
    speaking: bool = True
    cultural: bool = True
    vocabulary: bool = True
    grammar: bool = True
    syntax: bool = True
    pronunciation: bool = True
    listening: bool = True
