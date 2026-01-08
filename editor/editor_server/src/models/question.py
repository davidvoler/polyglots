from pydantic import BaseModel



class Question(BaseModel):
    id: int
    lesson_id: int
    course_id: int
    lang: str: str = ''
    to_lang: str: str = ''

class Option(BaseModel):
    text: str = ''
    correct: bool = False

class ExplanationQuestion(Question):
    qtype = 'explanation'
    title: str
    text: str

class SingleChoiceQuestion(Question):
    qtype = 'single_choice'
    sentence: str
    options: list[Option]
    voice: str = ''
    annotated_sentence: dict = {}

class MultipleChoiceQuestion(Question):
    qtype = 'multiple_choice'
    sentence: str
    options: list[Option]
    voice: str = ''
    annotated_sentence: dict = {}


class IdentifyWordsQuestion(Question):
    qtype = 'identify_words'
    sentence: str
    options: list[Option]
    voice: str = ''
    annotated_sentence: dict = {}
    multiple_choice: bool = True

class WordsArrayQuestion(Question):
    qtype = 'words_array'
    sentence: str
    options: list[Option]
    ab_array: list[str]

class MemoryGameQuestion(Question):
    qtype = 'memory_game'
    sentence: str
    letters: str
    view_seconds: int = 5

class TypeQuestion(Question):
    qtype = 'type'
    sentence: str
    letters: list[str]
    view_seconds: int = 5
