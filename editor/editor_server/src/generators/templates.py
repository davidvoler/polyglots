from pydantic import BaseModel
import random


class ModuleTemplate(BaseModel):
    words: int = 8
    level: int = 1
    lessons_types: list[str] = ['reading', 'listening', 'speaking', 'writing', 'grammar', 'syntax', 'culture', 'vocabulary', 'alphabet']
    lessons_content: list[str] = ['greetings', 'verbs', 'nouns', 'adjectives', 'adverbs', 'prepositions', 'conjunctions', 'pronouns', 'interjections','auxiliary_verbs']
    lessons_count: int = 20
    module_count: int = 5


class LessonTemplate(BaseModel):
    words: int = 8
    verbs: int = 4
    level: int = 1
    lessons_type:str = 'reading'



COURSE_TEMPLATE1 = [
    ModuleTemplate(words=10, level=1, lessons_types=['listening', 'vocabulary'], lessons_content=['greetings'], lessons_count=10, module_count=5),
    ModuleTemplate(words=15, level=2, lessons_types=['listening', 'vocabulary'], lessons_content=[ 'verbs', 'nouns',], lessons_count=10, module_count=5),
    ModuleTemplate(words=20, level=3, lessons_types=['listening', 'vocabulary'], lessons_content=[], lessons_count=10, module_count=5),
]



COURSE_TEMPLATE_JAPANESE = [
    ModuleTemplate(words=10, level=1, lessons_types=['listening', 'vocabulary'], lessons_content=['greetings'], lessons_count=10, module_count=5),
    ModuleTemplate(words=20, level=5, lessons_types=['listening', 'vocabulary'], lessons_content=[ 'verbs', 'nouns',], lessons_count=10, module_count=5),
    ModuleTemplate(words=15, level=10, lessons_types=['reading', 'alphabet'], lessons_content=[ 'hiragana'], lessons_count=10, module_count=5),
    ModuleTemplate(words=15, level=15, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives'], lessons_count=10, module_count=5),
    ModuleTemplate(words=15, level=20, lessons_types=['listening', 'vocabulary','reading'], lessons_content=[ 'verbs', 'nouns','adverbs'], lessons_count=10, module_count=5),
    ModuleTemplate(words=20, level=25, lessons_types=['reading', 'alphabet'], lessons_content=[ 'kanji',], lessons_count=10, module_count=5),
    ModuleTemplate(words=30, level=30, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs'], lessons_count=10, module_count=5),
    ModuleTemplate(words=20, level=35, lessons_types=['reading', 'alphabet'], lessons_content=[ 'kanji',], lessons_count=10, module_count=5),
    ModuleTemplate(words=30, level=40, lessons_types=['listening', 'vocabulary','reading'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing'], lessons_count=10, module_count=5),
    ModuleTemplate(words=20, level=45, lessons_types=['reading', 'alphabet', 'writing'], lessons_content=[ 'kanji',], lessons_count=10, module_count=5),
    ModuleTemplate(words=50, level=50, lessons_types=['listening', 'vocabulary','reading', 'writing'], lessons_content=[ 'katakana'], lessons_count=10, module_count=5),
    ModuleTemplate(words=50, level=55, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing'], lessons_count=10, module_count=5),
    ModuleTemplate(words=50, level=60, lessons_types=['grammar'], lessons_content=[ 'syntax', 'auxiliary_verbs'], lessons_count=10, module_count=5),
    ModuleTemplate(words=50, level=65, lessons_types=['grammar'], lessons_content=[ 'syntax', 'particles'], lessons_count=10, module_count=5),
    ModuleTemplate(words=50, level=70, lessons_types=['reading', 'alphabet', 'writing'], lessons_content=[ 'kanji',], lessons_count=10, module_count=5),
    ModuleTemplate(words=60, level=75, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing'], lessons_count=10, module_count=5),
    ModuleTemplate(words=70, level=80, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing'], lessons_count=10, module_count=5),
    ModuleTemplate(words=80, level=85, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing','grammar', 'syntax', 'kanji'], lessons_count=10, module_count=5),
    ModuleTemplate(words=90, level=90, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing','grammar', 'kanji'], lessons_count=10, module_count=5),
    ModuleTemplate(words=100, level=95, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing','syntax', 'kanji'], lessons_count=10, module_count=5),
    ModuleTemplate(words=200, level=100, lessons_types=['listening', 'vocabulary','reading', 'speaking'], lessons_content=[ 'verbs', 'nouns','adjectives','adverbs','writing','grammar', 'syntax', 'kanji'], lessons_count=10, module_count=5),
]


def gen_course_form_template(lang: str, to_lang: str):
    template = COURSE_TEMPLATE_JAPANESE
    module_count = 0
    for mt in template:
        for i in range(mt.module_count):
            module_count += 1
            print(f"Module: {module_count}  lessons_types: {mt.lessons_types}  lessons_content: {mt.lessons_content}")
            for lc in range(mt.lessons_count):

                print( f"    Lesson: {lc+1}  lessons_type: {random.choice(mt.lessons_types)}  lessons_content: {random.choice(mt.lessons_content)}")
            print("--------------------------------")



if __name__ == "__main__":
    gen_course_form_template("en", "ja")