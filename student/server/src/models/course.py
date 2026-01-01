from pydantic import BaseModel


class Lesson(BaseModel):
    id: int
    name: str
    description: str = ''
    image: str = ''

class Module(BaseModel):
    id: int
    name: str
    description: str = ''
    image: str = ''
    lessons: list[Lesson]

class Course(BaseModel):
    id: int
    lang: str
    to_lang: str
    name: str
    description: str = ''
    image: str = ''
    modules: list[Module]
    modules_count: int = 0
    lessons_count: int = 0



class CourseRequest(BaseModel):
    lang: str
    to_lang: str

