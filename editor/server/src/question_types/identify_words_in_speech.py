import random
from question_types.exercise_model import ExerciseModel, save_exercise_new_format

async def identify_words_in_speech(
    words:list, 
    text:str, 
    word_collections:list
):
    rnd = random.choices(word_collections, k=6)
    incorrect = []
    for ic in rnd:
        if ic not in text:
            incorrect.append(ic)
    return words,text,incorrect


async def create_identify_words_in_speech_exercise(exercise:ExerciseModel, words:list, text:str, word_collections:list):
    rnd = random.choices(word_collections, k=6)
    incorrect = []
    for ic in rnd:
        if ic not in text:
            incorrect.append(ic)
    exercise.exercise_type = 'identify_words_in_speech'
    exercise.correct_options = words
    exercise.wrong_options = incorrect
    await save_exercise_new_format(exercise)