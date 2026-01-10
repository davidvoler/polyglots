import random
from typing import List, Tuple
from question_types.exercise_model import ExerciseModel, save_exercise_new_format


async def type_question(exercise:ExerciseModel, word: str, letters: list[str]) -> int:
    exercise.extra_data["word"] = word
    exercise.extra_data["letters"] = letters
    exercise.exercise_type = 'type_question'
    await save_exercise_new_format(exercise)
    