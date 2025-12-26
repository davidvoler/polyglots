from generators.generate import gen_course
from generators.course_template import CourseTemplate
from models.generate import GeneratedCourse, GreetingModule, Module, Lesson
import asyncio
import os

os.environ["POSTGRES_PORT"] = "5433"  

def print_course(course: GeneratedCourse):
    """Print the generated course structure for review"""
    print("=" * 80)
    print(f"GENERATED COURSE: {course.lang} -> {course.to_lang}")
    print("=" * 80)
    
    # Print greeting module if present
    if course.greeting_module:
        print_greeting_module(course.greeting_module)
    
    # Print regular modules
    for module in course.modules:
        print_module(module)
    
    print("=" * 80)
    print(f"Course Summary: {len(course.modules)} modules")
    if course.greeting_module:
        print(f"  + 1 greeting module")
    print("=" * 80)


def print_greeting_module(module: GreetingModule):
    """Print greeting module"""
    print("\n" + "=" * 50)
    print(f"Module {module.module_number} - {module.module_type.upper()}")
    print("=" * 50)
    print(f"Words: {', '.join(module.words)}\n")
    
    for lesson in module.lessons:
        print_lesson(lesson)


def print_module(module: Module):
    """Print a module"""
    print("\n" + "-" * 70)
    print(f"Module {module.module_number}")
    print(f"Words: {', '.join(module.words)}")
    print(f"Sentence length range: {module.sentence_length_range[0]}-{module.sentence_length_range[1]}")
    print("-" * 70)
    
    # Print lessons
    if module.lessons:
        print("\nLessons:")
        for lesson in module.lessons:
            print_lesson(lesson)
    
    # Note: Reading and writing exercises are still printed by their functions
    # TODO: Add print functions for ReadingExercise and WritingExercise when refactored


def print_lesson(lesson: Lesson):
    """Print a lesson"""
    print(f"\n  Lesson {lesson.lesson_number}: {lesson.display_name}")
    if lesson.sentences:
        for sentence in lesson.sentences:
            print(f"    - {sentence.text} | {sentence.translation}")
    else:
        print(f"    (Placeholder lesson)")


async def test_gen_course():
    """Test function for course generation with CourseTemplate"""
    # Create a CourseTemplate instance
    course_template = CourseTemplate(
        lang='en',
        to_lang='ja',
        words_per_module_start=2,
        words_per_module_increase_factor=0.3,
        sentence_length_start=3,
        sentence_length_increase_factor=0.1,
        verbs=0.4,
        nouns=0.4,
        adjectives=0.1,
        adverbs=0.1,
        grammar_per_module=1,
        greeting_module=True,  # Enable greeting module
        reading_module=True,  # Enable reading module
        reading_exercises=True,  # Enable focused reading exercises
        writing_exercises=True  # Enable focused writing exercises
    )
    
    # Generate course and get the structure
    course = await gen_course(course_template)
    
    # Print the course for review
    print_course(course)

if __name__ == "__main__":
    asyncio.run(test_gen_course())