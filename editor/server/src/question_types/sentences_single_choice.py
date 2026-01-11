import random
from typing import List, Tuple
from question_types.exercise_model import ExerciseModel, save_exercise_new_format


async def single_choice_sentence(exercise:ExerciseModel, sentence: dict, to_sentence: dict) -> int:
    exercise.correct_options = [to_sentence.get('text')]
    exercise.wrong_options = to_sentence.get('options')
    exercise.exercise_type = 'sentence_single_choice'
    await save_exercise_new_format(exercise)
    