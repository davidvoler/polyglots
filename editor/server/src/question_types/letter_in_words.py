import random
from question_types.excercise_model import ExerciseModel


def letter_in_words(letter:str,words_collection:list, words_with_letter:list=[])->ExerciseModel:
    
    rnd = random.choices(words_collection, k=6)
    incorrect = []
    for ic in rnd:
        if letter not in ic:
            incorrect.append(ic)
    exercise = ExerciseModel(
        exercise_type="letter_in_words",
        letter=letter,
        correct_options=words_with_letter,
        wrong_options=incorrect
    )
    return exercise