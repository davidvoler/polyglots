"""This is an alternative templating approach"""
from pydantic import BaseModel
from utils.db import get_query_results
import importlib
from typing import Optional
from models.generate import Sentence, Lesson, Module, GreetingModule, WordWithType

class CourseTemplate(BaseModel):
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
    reading_exercises: bool = False  # Focused reading exercises for each module
    writing_exercises: bool = False  # Focused writing exercises for each module



def gen_course_based_on_copus():
    """Steps:
    1. Get verbs of sentences with up to 3 words - having more than 3 sentences per verb
    2. For japanese get the auxiliary verbs - prefer 1-2 simple once - like those indicating past and present 
    3. Create modules with this verbs until they are finished 
    4. do 1-3 for nouns in sentences up to 3 words
    5. Add explanation to different elements that are most common in the sentences selected so far 
      - for example in Japanese if we had 'ni' particle appearing 30 time explain the particle and how it is used 
    6. Now repeat this processes for sentences up to 4,5,6 words etc.
      - consider if we exclude verb that have already appeared in the previous modules - maybe not.
    7. add adjectives, adverbs, nouns, and search by them - prefer those seen already 
    
    """

    pass

    

def create_course_template(course_template: CourseTemplate):
    words_per_module = int(course_template.words_per_module_start)
    sentence_length = course_template.sentence_length_start
    for i in range(30):
        print(f"Module {i+1} - words: {int(words_per_module)} - sentence length: {int(sentence_length)}")
        words_per_module += course_template.words_per_module_increase_factor
        sentence_length += course_template.sentence_length_increase_factor

async def gen_lessons(lang: str, to_lang: str, from_ln: int, to_len: int, words: list[str | WordWithType], lessons_count: int) -> list[Lesson]:
    """
    Generate lessons for words and return Lesson objects.
    
    Returns:
        List of Lesson objects
    """
    lessons = []
    lesson_no = 0
    
    sql = """
    select l.text as text, tl.text as translation from content_raw.sentence_elements l 
    join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
    join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
    where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s and l.root = %s order by l.len_c limit 10
    """
    for word_item in words:
        # Handle both string and WordWithType objects
        if isinstance(word_item, WordWithType):
            word = word_item.word
            word_type = word_item.word_type
            display_name = f"{word} ({word_type})"
        else:
            word = word_item
            word_type = "unknown"
            display_name = word
        
        lesson_no += 1
        sentence_results = await get_query_results(sql, (lang, to_lang, from_ln, to_len, word))
        sentences = [
            Sentence(text=s.get('text'), translation=s.get('translation'))
            for s in sentence_results
        ]
        
        lessons.append(Lesson(
            lesson_number=lesson_no,
            word=word,
            word_type=word_type if word_type != "unknown" else None,
            display_name=display_name,
            sentences=sentences
        ))
    
    # Add placeholder lessons
    placeholders = [
        "Grammar explanation",
        "Cultural explanation",
    ]
    for placeholder in placeholders:
        lesson_no += 1
        lessons.append(Lesson(
            lesson_number=lesson_no,
            display_name=f"Placeholder: {placeholder}",
            sentences=[]
        ))
    
    return lessons
    
    
        


def get_greeting_words(lang: str) -> list[str]:
    """
    Get greeting words for a given language.
    
    Args:
        lang: Language code (e.g., 'en', 'ja')
    
    Returns:
        List of greeting words/phrases
    """
    try:
        module = importlib.import_module(f"generators.{lang}.greeting")
        return getattr(module, "GREETING_WORDS", [])
    except (ImportError, AttributeError):
        return []


async def gen_greeting_module(course_template: CourseTemplate) -> Optional[GreetingModule]:
    """
    Generate a greeting module with greeting words/phrases.
    
    Args:
        course_template: CourseTemplate instance with lang and to_lang
    
    Returns:
        GreetingModule object or None if no greeting words found
    """
    greeting_words = get_greeting_words(course_template.lang)
    if not greeting_words:
        return None
    
    # Generate lessons for greeting words
    lessons = await gen_lessons(
        course_template.lang, 
        course_template.to_lang, 
        1, 
        10,  # Allow longer sentences for greetings
        greeting_words, 
        len(greeting_words)
    )
    
    return GreetingModule(
        module_number=0,
        module_type="greeting",
        words=greeting_words,
        lessons=lessons
    )


async def gen_reading_lessons(lang: str, to_lang: str, from_ln: int, to_len: int, words: list[str | WordWithType]):
    """
    Generate reading lessons focusing on practicing reading the words and sentences.
    
    Args:
        lang: Source language code
        to_lang: Target language code for translations
        from_ln: Minimum sentence length
        to_len: Maximum sentence length
        words: List of words to practice reading
    """
    lesson_no = 0
    
    sql = """
    select l.text as text, tl.text as translation from content_raw.sentence_elements l 
    join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
    join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
    where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s and l.root = %s order by l.len_c limit 10
    """
    
    print("  --- Reading Practice ---")
    word_strings = []
    for word_item in words:
        # Handle both string and WordWithType objects
        if isinstance(word_item, WordWithType):
            word = word_item.word
            display_name = f"{word_item.word} ({word_item.word_type})"
            word_strings.append(word)
        else:
            word = word_item
            display_name = word
            word_strings.append(word)
        
        lesson_no += 1
        print(f"  Reading Lesson {lesson_no}: Practice reading '{display_name}'")
        sentences = await get_query_results(sql, (lang, to_lang, from_ln, to_len, word))
        for sentence in sentences:
            print(f"    Read: {sentence.get('text')} | Translation: {sentence.get('translation')}")
    
    # Add a combined reading exercise with all words
    if len(word_strings) > 1:
        lesson_no += 1
        # Create display names for the combined exercise
        display_names = []
        for word_item in words:
            if isinstance(word_item, WordWithType):
                display_names.append(f"{word_item.word} ({word_item.word_type})")
            else:
                display_names.append(str(word_item))
        print(f"  Reading Lesson {lesson_no}: Combined reading practice with words: {', '.join(display_names)}")
        # Get sentences containing any of the words from the module
        # Build OR conditions for each word
        word_conditions = " OR ".join(["l.root = %s"] * len(word_strings))
        combined_sql = f"""
        select l.text as text, tl.text as translation from content_raw.sentence_elements l 
        join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
        join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
        where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s 
        and ({word_conditions})
        order by l.len_c limit 5
        """
        combined_sentences = await get_query_results(combined_sql, (lang, to_lang, from_ln, to_len, *word_strings))
        for sentence in combined_sentences:
            print(f"    Read: {sentence.get('text')} | Translation: {sentence.get('translation')}")


async def gen_reading_exercises(lang: str, to_lang: str, from_ln: int, to_len: int, words: list[str | WordWithType]):
    """
    Generate focused reading exercises concentrating on reading the new words and sentences in the module.
    These exercises are more structured and focused on comprehension practice.
    
    Args:
        lang: Source language code
        to_lang: Target language code for translations
        from_ln: Minimum sentence length
        to_len: Maximum sentence length
        words: List of words (with types) introduced in this module
    """
    # Extract word strings and create display names
    word_strings = []
    word_display_map = {}
    for word_item in words:
        if isinstance(word_item, WordWithType):
            word = word_item.word
            display_name = f"{word_item.word} ({word_item.word_type})"
            word_strings.append(word)
            word_display_map[word] = display_name
        else:
            word = word_item
            display_name = word
            word_strings.append(word)
            word_display_map[word] = display_name
    
    if not word_strings:
        return
    
    print("\n  ===== Reading Exercises =====\n")
    
    # Exercise 1: Word Recognition - Read sentences containing each new word
    print("  Exercise 1: Word Recognition")
    print("  Read the following sentences and identify the new words:\n")
    
    word_recognition_sql = """
    select l.text as text, tl.text as translation, l.root as root_word
    from content_raw.sentence_elements l 
    join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
    join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
    where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s and l.root = %s 
    order by l.len_c limit 5
    """
    
    exercise_sentences = []
    for word in word_strings:
        sentences = await get_query_results(word_recognition_sql, (lang, to_lang, from_ln, to_len, word))
        for sentence in sentences:
            exercise_sentences.append({
                'text': sentence.get('text'),
                'translation': sentence.get('translation'),
                'target_word': word,
                'display_word': word_display_map.get(word, word)
            })
    
    # Display sentences with target words highlighted
    for i, sent in enumerate(exercise_sentences[:10], 1):
        print(f"    {i}. Read: {sent['text']}")
        print(f"       Target word: {sent['display_word']}")
        print(f"       Translation: {sent['translation']}\n")
    
    # Exercise 2: Reading Comprehension - Sentences with multiple new words
    print("  Exercise 2: Reading Comprehension")
    print("  Read sentences containing multiple new words and practice comprehension:\n")
    
    if len(word_strings) > 1:
        # Get sentences that contain multiple words from the module
        word_conditions = " OR ".join(["l.root = %s"] * len(word_strings))
        comprehension_sql = f"""
        select l.text as text, tl.text as translation, l.root as root_word
        from content_raw.sentence_elements l 
        join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
        join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
        where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s 
        and ({word_conditions})
        order by l.len_c limit 8
        """
        
        comprehension_sentences = await get_query_results(
            comprehension_sql, 
            (lang, to_lang, from_ln, to_len, *word_strings)
        )
        
        for i, sentence in enumerate(comprehension_sentences, 1):
            # Find which words appear in this sentence
            sentence_text = sentence.get('text', '').lower()
            found_words = []
            for word in word_strings:
                if word.lower() in sentence_text:
                    found_words.append(word_display_map.get(word, word))
            
            print(f"    {i}. Read: {sentence.get('text')}")
            if found_words:
                print(f"       Contains words: {', '.join(found_words)}")
            print(f"       Translation: {sentence.get('translation')}\n")
    
    # Exercise 3: Word Type Practice - Group sentences by word type
    print("  Exercise 3: Word Type Practice")
    print("  Practice reading sentences grouped by word type:\n")
    
    # Group words by type
    words_by_type = {}
    for word_item in words:
        if isinstance(word_item, WordWithType):
            wtype = word_item.word_type
            if wtype not in words_by_type:
                words_by_type[wtype] = []
            words_by_type[wtype].append(word_item.word)
        else:
            if 'unknown' not in words_by_type:
                words_by_type['unknown'] = []
            words_by_type['unknown'].append(word_item)
    
    for wtype, type_words in words_by_type.items():
        print(f"    {wtype.capitalize()}s:")
        for word in type_words[:3]:  # Limit to 3 examples per type
            sentences = await get_query_results(word_recognition_sql, (lang, to_lang, from_ln, to_len, word))
            if sentences:
                sent = sentences[0]
                print(f"      - {sent.get('text')} ({sent.get('translation')})")
        print()
    
    print("  ===== End Reading Exercises =====\n")


async def gen_writing_exercises(lang: str, to_lang: str, from_ln: int, to_len: int, words: list[str | WordWithType]):
    """
    Generate focused writing exercises concentrating on writing with the new words and sentences in the module.
    These exercises help students practice writing using the new vocabulary.
    
    Args:
        lang: Source language code (target language for writing)
        to_lang: Translation language code
        from_ln: Minimum sentence length
        to_len: Maximum sentence length
        words: List of words (with types) introduced in this module
    """
    # Extract word strings and create display names
    word_strings = []
    word_display_map = {}
    for word_item in words:
        if isinstance(word_item, WordWithType):
            word = word_item.word
            display_name = f"{word_item.word} ({word_item.word_type})"
            word_strings.append(word)
            word_display_map[word] = display_name
        else:
            word = word_item
            display_name = word
            word_strings.append(word)
            word_display_map[word] = display_name
    
    if not word_strings:
        return
    
    print("\n  ===== Writing Exercises =====\n")
    
    # Get example sentences for writing practice
    example_sql = """
    select l.text as text, tl.text as translation, l.root as root_word
    from content_raw.sentence_elements l 
    join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
    join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
    where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s and l.root = %s 
    order by l.len_c limit 3
    """
    
    # Exercise 1: Word Writing Practice - Write sentences using each new word
    print("  Exercise 1: Word Writing Practice")
    print("  Write sentences using each new word:\n")
    
    for i, word in enumerate(word_strings, 1):
        display_name = word_display_map.get(word, word)
        print(f"    {i}. Write a sentence using the word: {display_name}")
        
        # Show example sentences as reference
        examples = await get_query_results(example_sql, (lang, to_lang, from_ln, to_len, word))
        if examples:
            print(f"       Examples:")
            for j, ex in enumerate(examples[:2], 1):
                print(f"         {j}. {ex.get('text')} ({ex.get('translation')})")
        print(f"       Your sentence: _______________\n")
    
    # Exercise 2: Translation Writing - Write from translation
    print("  Exercise 2: Translation Writing")
    print("  Write sentences in the target language based on translations:\n")
    
    if len(word_strings) > 0:
        for word in word_strings[:3]:  # Limit to 3 exercises
            examples = await get_query_results(example_sql, (lang, to_lang, from_ln, to_len, word))
            if examples:
                ex = examples[0]
                print(f"    Translate and write: {ex.get('translation')}")
                print(f"       Write in {lang}: _______________")
                print(f"       Answer: {ex.get('text')}\n")
    
    # Exercise 3: Word Type Writing - Write sentences by word type
    print("  Exercise 3: Word Type Writing")
    print("  Write sentences using words grouped by type:\n")
    
    # Group words by type
    words_by_type = {}
    for word_item in words:
        if isinstance(word_item, WordWithType):
            wtype = word_item.word_type
            if wtype not in words_by_type:
                words_by_type[wtype] = []
            words_by_type[wtype].append(word_item.word)
        else:
            if 'unknown' not in words_by_type:
                words_by_type['unknown'] = []
            words_by_type['unknown'].append(word_item)
    
    for wtype, type_words in words_by_type.items():
        print(f"    {wtype.capitalize()}s:")
        for word in type_words[:2]:  # Limit to 2 examples per type
            display_name = word_display_map.get(word, word)
            print(f"      - Write a sentence with: {display_name}")
            examples = await get_query_results(example_sql, (lang, to_lang, from_ln, to_len, word))
            if examples:
                print(f"        Example: {examples[0].get('text')}")
            print()
    
    # Exercise 4: Combined Writing - Write sentences using multiple new words
    if len(word_strings) > 1:
        print("  Exercise 4: Combined Writing")
        print("  Write sentences using multiple new words from this module:\n")
        
        # Get sentences with multiple words
        word_conditions = " OR ".join(["l.root = %s"] * len(word_strings))
        combined_sql = f"""
        select l.text as text, tl.text as translation
        from content_raw.sentence_elements l 
        join content_raw.translation_links tr on l.lang = tr.lang and l.id = tr.id
        join content_raw.sentence_elements tl on tr.to_id = tl.id and tr.to_lang = tl.lang
        where l.lang=%s and tr.to_lang=%s and l.len_elm >= %s and l.len_elm <= %s 
        and ({word_conditions})
        order by l.len_c limit 3
        """
        
        combined_sentences = await get_query_results(
            combined_sql, 
            (lang, to_lang, from_ln, to_len, *word_strings)
        )
        
        display_names = [word_display_map.get(w, w) for w in word_strings]
        print(f"    Use these words: {', '.join(display_names)}\n")
        
        for i, sentence in enumerate(combined_sentences, 1):
            print(f"    {i}. Write a sentence using at least 2 of the words above.")
            print(f"       Example: {sentence.get('text')} ({sentence.get('translation')})")
            print(f"       Your sentence: _______________\n")
    
    print("  ===== End Writing Exercises =====\n")


async def create_course_template_with_words(course_template: CourseTemplate, words: list[str | WordWithType]) -> list[Module]:
    """
    Create modules from words and return Module objects.
    
    Returns:
        List of Module objects
    """
    modules = []
    words_per_module = course_template.words_per_module_start
    sentence_length = course_template.sentence_length_start
    i = 0
    
    while len(words) > 0:
        i += 1
        module_words = words[:int(words_per_module)]
        words = words[int(words_per_module):]
        
        # Format module words for display and extract WordWithType objects
        module_words_display = []
        words_with_types = []
        for word_item in module_words:
            if isinstance(word_item, WordWithType):
                module_words_display.append(f"{word_item.word} ({word_item.word_type})")
                words_with_types.append(word_item)
            else:
                module_words_display.append(str(word_item))
                words_with_types.append(WordWithType(word=str(word_item), word_type="unknown"))
        
        # Generate regular lessons for the module
        lessons = await gen_lessons(
            course_template.lang, 
            course_template.to_lang, 
            1, 
            int(sentence_length), 
            module_words, 
            10
        )
        
        # For now, reading/writing exercises are still printed (can be refactored later)
        # Generate reading lessons if enabled
        reading_exercises = []
        if course_template.reading_module:
            # TODO: Refactor gen_reading_lessons to return ReadingExercise objects
            await gen_reading_lessons(
                course_template.lang, 
                course_template.to_lang, 
                1, 
                int(sentence_length), 
                module_words
            )
        
        # Generate focused reading exercises if enabled
        if course_template.reading_exercises:
            # TODO: Refactor gen_reading_exercises to return ReadingExercise objects
            await gen_reading_exercises(
                course_template.lang,
                course_template.to_lang,
                1,
                int(sentence_length),
                module_words
            )
        
        # Generate focused writing exercises if enabled
        writing_exercises = []
        if course_template.writing_exercises:
            # TODO: Refactor gen_writing_exercises to return WritingExercise objects
            await gen_writing_exercises(
                course_template.lang,
                course_template.to_lang,
                1,
                int(sentence_length),
                module_words
            )
        
        modules.append(Module(
            module_number=i,
            words=module_words_display,
            words_with_types=words_with_types,
            sentence_length_range=(1, int(sentence_length)),
            lessons=lessons,
            reading_exercises=reading_exercises,
            writing_exercises=writing_exercises
        ))
        
        words_per_module += course_template.words_per_module_increase_factor
        sentence_length += course_template.sentence_length_increase_factor
    
    return modules





if __name__ == "__main__":
    course_template = CourseTemplate(
        lang='en',
        to_lang='ja'
    )
    create_course_template(course_template)