import random
from question_types.exercise_model import ExerciseModel, save_exercise_new_format


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


async def create_letter_in_words_exercise(exercise:ExerciseModel, letter:str, words_with_letter:list,words_collection:list):
    k = min(8, len(words_collection))
    rnd = random.choices(words_collection, k=k)
    incorrect = []
    for ic in rnd:
        if letter not in ic:
            incorrect.append(ic)
    exercise.correct_options = words_with_letter
    exercise.wrong_options = incorrect
    exercise.exercise_type = 'letter_in_words'
    await save_exercise_new_format(exercise)