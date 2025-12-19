"""This is an alternative templating approach"""
from pydantic import BaseModel

class CourseTemplate(BaseModel):
    words_per_module_start: float =2
    words_per_module_increase_factor: float = 0.3
    sentence_length_start: int = 3
    sentence_length_increase_factor: float = 0.1
    verbs: int = 0.4
    nouns: int = 0.4
    adjectives: int = 0.1
    adverbs: int = 0.1
    grammar_per_module: int = 1



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

def create_course_template_with_words(course_template: CourseTemplate, words: list[str]):
    words_per_module = course_template.words_per_module_start
    sentence_length = course_template.sentence_length_start
    i = 0
    while len(words) > 0:
        i += 1
        module_words = words[:int(words_per_module)]
        words = words[int(words_per_module):]
        print(f"Module {i+1} - words: {module_words} - sentence length: {int(sentence_length)}")
        words_per_module += course_template.words_per_module_increase_factor
        sentence_length += course_template.sentence_length_increase_factor





if __name__ == "__main__":
    course_template = CourseTemplate()
    create_course_template(course_template)