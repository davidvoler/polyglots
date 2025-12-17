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



class CourseTemplate(BaseModel):
    name: str
    description: str
    modules: list[ModuleTemplate]
    def get_template_data(self):
        module_count = 0
        lesson_count = 0
        lessons_types = set()
        lessons_content = set()
        for mt in self.modules:
            module_count += mt.module_count
            lesson_count += mt.lessons_count * mt.module_count
            lessons_types.update(mt.lessons_types)
            lessons_content.update(mt.lessons_content)
        

        
        return {
            "name": self.name,
            "description": self.description,
            "modules_groups": len(self.modules),
            "modules_count": module_count,
            "lessons_count": lesson_count,
            "lessons_types": list(lessons_types),
            "lessons_content": list(lessons_content),
        }


COURSE_TEMPLATE1 = [
    ModuleTemplate(words=10, level=1, lessons_types=['listening', 'vocabulary'], lessons_content=['greetings'], lessons_count=10, module_count=5),
    ModuleTemplate(words=15, level=2, lessons_types=['listening', 'vocabulary'], lessons_content=[ 'verbs', 'nouns',], lessons_count=10, module_count=5),
    ModuleTemplate(words=20, level=3, lessons_types=['listening', 'vocabulary'], lessons_content=[], lessons_count=10, module_count=5),
]




COURSE_TEMPLATE_JAPANESE = CourseTemplate(
    name="Japanese Course",
    description="A course for learning Japanese including learning to read and write Hiragana, Kanji and Katakana",
    modules=[
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
)


def gen_course_form_template(lang: str, to_lang: str):
    template = COURSE_TEMPLATE_JAPANESE.modules
    module_count = 0
    for mt in template:
        lesson_count = 0
        for _ in range(mt.module_count):
            module_count += 1
            print(f"Module: {module_count}  lessons_types: {mt.lessons_types}  lessons_content: {mt.lessons_content}")
            for lc in range(mt.lessons_count):
                lesson_count+=1
                lesson_type = mt.lessons_types[lesson_count%len(mt.lessons_types)]
                lesson_content = mt.lessons_content[lesson_count%len(mt.lessons_content)]
                print( f"    Lesson: {lc+1}  lessons_type: {lesson_type}  lessons_content: {lesson_content}")
            print( f"    Lesson: {lc+2}  lessons_type: module recap")
            print("--------------------------------")



def get_template_data(template: list[ModuleTemplate]):
    pass 


if __name__ == "__main__":

    print(COURSE_TEMPLATE_JAPANESE.get_template_data())
    gen_course_form_template("en", "ja")