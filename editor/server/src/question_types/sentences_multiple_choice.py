import random
from typing import List, Tuple
from question_types.exercise_model import ExerciseModel, save_exercise_new_format


async def multiple_choice_sentence(exercise:ExerciseModel, word: str, letters: list[str]) -> int:
    exercise.correct_options = [word]
    exercise.wrong_options = [word]
    exercise.exercise_type= 'sentence_multiple_choice'
    await save_exercise_new_format(exercise)