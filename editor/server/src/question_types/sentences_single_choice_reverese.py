import random
from typing import List, Tuple
from question_types.exercise_model import ExerciseModel, save_exercise_new_format


async def single_choice_sentence_reverse(exercise:ExerciseModel, word: str, letters: list[str]) -> int:
    exercise.correct_options = [word]
    exercise.wrong_options = [word]
    exercise.exercise_type = 'sentence_single_choice'
    await save_exercise_new_format(exercise)
    