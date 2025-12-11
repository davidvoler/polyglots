from pydantic import BaseModel
from datetime import datetime




class Question(BaseModel):
    id: int
    step_id: int
    sentence_id: int
    explanation: str = ''
    weight: int = 0


class Step(BaseModel):
    id: int
    lesson_id: int
    name: str
    description: str = ''
    created_by: str
    school: str = ''
    public: bool = True
    reviewed: bool = False
    questions: list[Question]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Lesson(BaseModel):
    id: int
    course_id: int
    name: str
    description: str = ''
    created_by: str
    school: str = ''
    public: bool = True
    reviewed: bool = False
    steps: list[Step]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Course(BaseModel):
    id: int
    name: str
    description: str = ''
    lang: str
    to_lang: str
    created_by: str
    school: str = ''
    public: bool = True
    reviewed: bool = False
    lessons: list[Lesson]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class CourseRequest(BaseModel):
    lang: str
    to_lang: str
    name: str
    description: str = ''
    limit: int = 300
    offset: int = 0
    created_by: str
    school: str = ''

class GenerateRequest(BaseModel):
    lang: str
    to_lang: str
    name: str
    description: str = ''
    created_by: str
    school: str = ''
    level: int = 0
    words: list[str]
    verbs: list[str]

class GenerateLessonsRequest(GenerateRequest):
    course_id: int
    lesson_count: int
    
class GenerateQuestionRequest(GenerateRequest):
    lesson_id: int
    step_count: int