from pydantic import BaseModel
from typing import Optional


class WordWithType(BaseModel):
    """Represents a word with its type (e.g., verb, noun, adjective)"""
    word: str
    word_type: str  # verb, noun, adjective, adverb, auxiliary_verb, etc.
    count: Optional[int] = None  # Number of sentences containing this word
    
    def __str__(self):
        return f"{self.word} ({self.word_type})"


class Sentence(BaseModel):
    """A sentence with its translation"""
    text: str
    translation: str


class Lesson(BaseModel):
    """A lesson introducing a word or concept"""
    lesson_number: int
    word: Optional[str] = None
    word_type: Optional[str] = None
    display_name: str
    sentences: list[Sentence] = []


class ReadingExercise(BaseModel):
    """A reading exercise"""
    exercise_type: str  # "word_recognition", "comprehension", "word_type", "combined"
    title: str
    sentences: list[Sentence] = []
    target_words: list[str] = []
    word_types: Optional[dict[str, list[str]]] = None


class WritingExercise(BaseModel):
    """A writing exercise"""
    exercise_type: str  # "word_practice", "translation", "word_type", "combined"
    title: str
    instruction: str
    example_sentences: list[Sentence] = []
    target_words: list[str] = []
    word_types: Optional[dict[str, list[str]]] = None


class Module(BaseModel):
    """A course module containing lessons and exercises"""
    module_number: int
    words: list[str]  # Display names of words
    words_with_types: list[WordWithType] = []
    sentence_length_range: tuple[int, int]  # (min, max)
    lessons: list[Lesson] = []
    reading_exercises: list[ReadingExercise] = []
    writing_exercises: list[WritingExercise] = []


class GreetingModule(BaseModel):
    """A greeting module (Module 0)"""
    module_number: int = 0
    module_type: str = "greeting"
    words: list[str]
    lessons: list[Lesson] = []


class GeneratedCourse(BaseModel):
    """A complete generated course structure"""
    lang: str
    to_lang: str
    greeting_module: Optional[GreetingModule] = None
    modules: list[Module] = []


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


class CourseTemplateRequest(BaseModel):
    """Request model for course generation matching CourseTemplate"""
    lang: str
    to_lang: str
    words_per_module_start: float = 2
    words_per_module_increase_factor: float = 0.3
    sentence_length_start: int = 3
    sentence_length_increase_factor: float = 0.1
    verbs: float = 0.4
    nouns: float = 0.4
    adjectives: float = 0.1
    adverbs: float = 0.1
    grammar_per_module: int = 1
    greeting_module: bool = False
    reading_module: bool = False
    reading_exercises: bool = False
    writing_exercises: bool = False
