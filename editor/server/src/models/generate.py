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


# --- Editor flow: course options, words, sentences, question types ---

class LanguageOption(BaseModel):
    code: str
    name: str


class QuestionTypeOption(BaseModel):
    id: str
    name: str
    description: str = ''
    applicable_to: str = 'sentence'  # 'sentence' | 'alphabet'


class CourseOptionsResponse(BaseModel):
    """Available languages and question types for course creation"""
    languages: list[LanguageOption] = []
    question_types: list[QuestionTypeOption] = []


class SentencesForWordRequest(BaseModel):
    lang: str
    to_lang: str
    word: str
    limit: int = 30


class SentenceForWordItem(BaseModel):
    id: int
    to_id: int = 0
    sentence: str
    translation: str
    options: list[str] = []
    len_elm: int = 0  # sentence length for ordering


class SentencesForWordResponse(BaseModel):
    word: str
    lang: str
    to_lang: str
    sentences: list[SentenceForWordItem] = []


class CreateCourseFromEditorRequest(BaseModel):
    """Create course from editor: options, words, sentences per word, question types, grouping"""
    title: str = ''
    description: str = ''
    lang: str
    to_lang: str
    selected_words: list[str] = []  # ordered list of words
    sentences_per_word: dict[str, list[int]] = {}  # word -> list of sentence ids (from sentence_elements.id)
    enabled_question_types: list[str] = []
    automate_lesson: bool = False  # if True: 15 shortest sentences, 15 single_choice + 5 identify_words
    lessons_per_module: int = 10  # group lessons into modules of this size


# --- Editor draft: save/resume wizard at last position ---

class EditorDraftWord(BaseModel):
    word: str
    weight: int


class SaveEditorDraftRequest(BaseModel):
    """Save or update editor wizard state."""
    title: str = ''
    description: str = ''
    lang: str
    to_lang: str
    selected_question_type_ids: list[str] = []
    words_with_weight: list[EditorDraftWord] = []  # ordered by weight
    step: int = 0
    automate_lesson: bool = False
    lessons_per_module: int = 10
    sentences_per_word: dict[str, list[int]] = {}


class EditorDraftResponse(BaseModel):
    """Full draft for resuming."""
    id: int
    created_at: str = ''
    updated_at: str = ''
    title: str = ''
    description: str = ''
    lang: str
    to_lang: str
    selected_question_type_ids: list[str] = []
    words_with_weight: list[EditorDraftWord] = []
    step: int = 0
    automate_lesson: bool = False
    lessons_per_module: int = 10
    sentences_per_word: dict[str, list[int]] = {}


class EditorDraftListItem(BaseModel):
    """Summary for list of drafts."""
    id: int
    title: str
    updated_at: str
    step: int
    lang: str
    to_lang: str


# --- Lesson wizard: generate questions from selected sentences, save lesson ---

class SentenceIdPair(BaseModel):
    sentence_id: int
    to_id: int


class GenerateQuestionsRequest(BaseModel):
    """Selected sentences for a word; server returns preview of generated exercises."""
    lang: str
    to_lang: str
    word: str
    sentences: list[SentenceIdPair]  # user-selected sentence + translation ids


class GeneratedExercisePreview(BaseModel):
    """One exercise as preview (not yet saved)."""
    exercise_type: str  # sentence_single_choice, identify_words_in_speech, etc.
    sentence: str = ''
    to_sentence: str = ''
    correct_options: list[str] = []
    wrong_options: list[str] = []
    sentence_id: int = 0
    to_sentence_id: int = 0
    extra_data: dict = {}
    is_duplicate: bool = False  # True when another exercise shares the same to_sentence_id in the module
    audio_link: str = ''


class GenerateQuestionsResponse(BaseModel):
    word: str
    exercises: list[GeneratedExercisePreview] = []


class SaveLessonRequest(BaseModel):
    """Save one lesson (word) with selected exercises. Create course/module if course_id is 0."""
    course_id: int = 0  # 0 = create new course and module
    module_id: int = 0
    lang: str
    to_lang: str
    word: str
    title: str = ''  # default to word
    description: str = ''
    course_title: str = ''  # used when creating course
    course_description: str = ''
    lessons_per_module: int = 10
    word_index: int = 0  # which word in the list (for module placement)
    exercises: list[GeneratedExercisePreview] = []  # user-selected subset


class SaveLessonResponse(BaseModel):
    course_id: int
    module_id: int
    lesson_id: int


# --- Module exercises: generate all exercises for a module in one call ---

class ModuleExercisesRequest(BaseModel):
    """Generate exercises for a whole module (multiple words) at once."""
    lang: str
    to_lang: str
    words: list[str]
    question_types: list[str] = []  # empty = all types
    sentences_per_word: int = 20


class WordExercisesResult(BaseModel):
    word: str
    exercises: list[GeneratedExercisePreview] = []


class ModuleExercisesResponse(BaseModel):
    lang: str
    to_lang: str
    results: list[WordExercisesResult] = []


# --- Course detail: full course tree for review screen ---

class ExerciseDetail(BaseModel):
    id: int
    exercise_type: str
    sentence: str = ''
    to_sentence: str = ''
    sentence_id: int = 0
    to_sentence_id: int = 0
    correct_options: list[str] = []
    wrong_options: list[str] = []


class LessonDetail(BaseModel):
    id: int
    title: str
    exercises: list[ExerciseDetail] = []


class ModuleDetail(BaseModel):
    id: int
    title: str
    lessons: list[LessonDetail] = []


class CourseDetail(BaseModel):
    id: int
    title: str
    description: str = ''
    lang: str
    to_lang: str
    modules: list[ModuleDetail] = []


class DeleteExercisesRequest(BaseModel):
    exercise_ids: list[int]
