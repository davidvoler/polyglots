from pydantic import BaseModel


class Lesson(BaseModel):
    lesson_id: int = 0
    course_id: int = 0
    module_id: int = 0
    lang: str = ''
    to_lang: str = ''
    title: str = ''
    description: str = ''
    image: str = ''

class Module(BaseModel):
    module_id: int = 0
    course_id: int = 0
    lang: str = ''
    to_lang: str = ''
    title: str = ''
    description: str = ''
    image: str = ''
    lessons: list[Lesson] = []
    lessons_count: int = 0

class Course(BaseModel):
    course_id: int = 0
    lang: str = ''
    to_lang: str = ''
    title: str = ''
    description: str = ''
    image: str = ''
    modules: list[Module] = []
    modules_count: int = 0
    lessons_count: int = 0



class CourseRequest(BaseModel):
    lang: str
    to_lang: str

