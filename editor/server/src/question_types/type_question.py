import random
from typing import List, Tuple
from question_types.exercise_model import ExerciseModel, save_exercise_new_format


async def type_question(exercise:ExerciseModel, word: str, letters: list[str]) -> int:
    random.shuffle(letters)
    keyboard= letters[:10] + list(word)
    random.shuffle(keyboard)
    exercise.extra_data["word"] = word
    exercise.extra_data["keyboard"] = keyboard
    exercise.exercise_type = 'type_question'
    await save_exercise_new_format(exercise)
    