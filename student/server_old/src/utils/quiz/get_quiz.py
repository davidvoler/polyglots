from models.quiz import Quiz, QuizRequest
from utils.scale import scale
from utils.users import get_or_create_user_vocab, update_or_create_user_vocab
from utils.stats import get_step_stats
from models.user_vocab import UserVocab
from utils.quiz.quiz_query_step import (
    get_step,
    get_parts_by_ids,
    get_lines_by_ids,
    get_by_dialogue,
    get_refresh,
    get_parts_by_words,
    get_parts_by_user_words,
)
from utils.users import get_or_create_user_vocab
from models.modes import PracticeMode
from utils.quiz.format import format_quiz
import asyncio
import random
from models.enums import ModeEnum, LevelEnum, CurrentPracticeEnum


def get_len_by_mark(times:int, mark:float, step_len=80) -> int:
    if not mark:
        return 80
    return  int(round(scale(mark, 0.4, 1.0, step_len, 35), 0))
    


def should_change_step(times:int, mark:float, step_len=80) -> bool:
    if not times or not mark:
        return False
    # print(f"should_change_step: {times} {mark}")
    times_by_mark = int(round(scale(mark, 0.4, 1.0, step_len, 35), 0))
    print(f"should_change_step: {times} {mark} {times_by_mark}")
    if times > times_by_mark:
        return True
    return False

def get_step_len(step):
    w_count = len(step.get('words', 0))
    d_count = len(step.get('dialogues', 0))
    l_count = len(step.get('lines', 0))
    p_count = len(step.get('parts', 0))
    s_count = len(step.get('structure', 0))
    step_len = max(int(w_count +l_count + p_count + s_count + d_count),100)
    return step_len

def get_available_step_modes(step:dict) -> list:
    steps = []
    try:
        if len(step.get('words', [])) > 0:
            steps.append(PracticeMode.words)
    except Exception as e:
        pass 
    try:
        if len(step.get('parts', [])) > 0:
            steps.append(PracticeMode.step)
    except Exception as e:
        pass 
    try:
        if len(step.get('structure', [])) > 0:
            steps.append(PracticeMode.structure)
    except Exception as e:
        pass
    try:
        if len(step.get('lines', [])) > 0:
            steps.append(PracticeMode.dialogue_lines)
    except Exception as e:
        pass
    try:
        if len(step.get('dialogues', [])) > 0:
            steps.append(PracticeMode.dialogue)
    except Exception as e:
        pass
    steps.append(PracticeMode.refresh)
    return steps

def get_next_mode(step,current_mode):
    if not current_mode:
        current_mode = PracticeMode.step
    modes = get_available_step_modes(step)
    print(f"get_next_mode: {modes} {current_mode}")
    try:
        current_index = modes.index(current_mode)
    except Exception as e:
        current_index = -1
    if current_index < 0:
        return random.choice(modes)
    next_index = (current_index + 1) % len(modes)
    #print(f"get_next_mode: {modes[next_index]} {modes}")
    # return random.choice(modes)
    return modes[next_index]




async def get_quiz(q:QuizRequest) -> Quiz:
    # print(f"get_quiz: {q}")
    """
    Get a quiz for a user
    """
    if not q.practice_type:
        q.practice_type = CurrentPracticeEnum.step.name
    if not q.practice_id:
        q.practice_id = "6"
    step_stats = await get_step_stats(q.user_id, q.lang, q.practice_id)
    print(f"get_quiz: {q}")
    if not q.practice_id:
        uv = await get_or_create_user_vocab(q.user_id, q.lang)
        q.practice_id = uv.current_practice_id
    if len(step_stats) > 0:
        q.practice_times = step_stats[0].get('times', 0)
        q.practice_mark = step_stats[0].get('mark', 0)
        if not q.practice_mark:
            q.practice_mark = 0.0
        if not q.practice_times:
            q.practice_times = 0
        if q.practice_times > 0:
            q.accuracy = q.practice_mark / q.practice_times
        else:
            q.accuracy = 0.0

    else:
        q.practice_times = 0
        q.practice_mark = 0.0
        q.accuracy = 0.0
    min_mark_practice = scale(q.mark, 0.4, 1.0, 4.0, 1.0)
    min_mark_refresh = scale(q.mark,  0.4, 1.0, 6.0, 2.4)
    min_word_practice = scale(q.mark,  0.4, 1.0, 6.5, 3.4)
    quiz_data = []
    # print (f"get_quiz: {q.user_id} {q.lang}")
    should_skip = should_change_step(q.practice_times, q.accuracy)
    # print('----------------------')
    # print (f"should_skip: {should_skip} {q.practice_times} {q.accuracy}")
    # print('----------------------')
    if should_skip:
        q.practice_id =  str(int(q.practice_id) + 1)
        q.practice_times = 0
        q.practice_mark = 0.0
        # q.last_mode = PracticeMode.refresh 
    # print (f"practice_id: {q.practice_id}, lang: {q.lang}")
    step = await get_step(q.practice_id, q.lang)
    # print (f"$$$$$$$$$$: {step}")
    
    q.last_mode = get_next_mode(step, q.last_mode)
    if q.last_mode == PracticeMode.words:
        parts = step.get('parts', [])
        words = step.get('words', [])
        #quiz_data =  await get_parts_by_words(q.user_id,q.lang, q.to_lang,min_mark_practice, parts, words)
        quiz_data =  await  get_parts_by_user_words(q.user_id, q.lang, q.to_lang, min_word_practice)
    elif q.last_mode == PracticeMode.step:
        parts = step.get('parts', [])
        quiz_data =  await get_parts_by_ids(q.user_id,q.lang, q.to_lang,min_mark_practice, parts)
    elif q.last_mode == PracticeMode.structure:
        parts = step.get('structure', [])
        quiz_data =  await get_parts_by_ids(q.user_id,q.lang, q.to_lang,min_mark_practice, parts)
    elif q.last_mode == PracticeMode.dialogue_lines:
        lines = step.get('lines', [])
        quiz_data =  await get_lines_by_ids(q.user_id,q.lang, q.to_lang, lines, min_mark_practice)
    elif q.last_mode == PracticeMode.dialogue:
        dialogues = step.get('dialogues', [])
        quiz_data =  await get_by_dialogue(q.lang, q.to_lang, dialogues)
    elif q.last_mode == PracticeMode.refresh:
        quiz_data =  await get_refresh(q.user_id, q.lang, q.to_lang, min_mark_refresh)
    if len(quiz_data) < 5:
        parts = step.get('parts', [])
        quiz_data =  await get_parts_by_ids(q.user_id,q.lang, q.to_lang,min_mark_practice, parts)
    if q.last_mode != PracticeMode.dialogue:
        quiz_data = quiz_data[:10]
    
    quiz = format_quiz(q.lang, q.to_lang, quiz_data, q.last_mode,  q.reverse_mode)
    # todo: add statistical data
    

    quiz.accuracy = q.accuracy
    quiz.practice_times = q.practice_times
    quiz.practice_mark = q.practice_mark
    quiz.accuracy = q.accuracy
    quiz.practice_id=q.practice_id,
    quiz.practice_type=q.practice_type
    quiz.practice_id = q.practice_id
    quiz.mode = q.last_mode
    
    quiz.change_step = should_skip
    quiz.remaining = get_len_by_mark(q.practice_times, q.accuracy) - q.practice_times
    
    # print(quiz)
    uv = UserVocab(
        user_id=q.user_id,
        lang=q.lang,
        to_lang=q.to_lang,
        last_step=q.practice_id,
        last_mode=q.last_mode.name,
        practice_times=q.practice_times,
        practice_mark=q.practice_mark,
        mark=q.mark,
        current_practice_type=q.practice_type,
        current_practice_id=q.practice_id,
    )
    # print(uv)
    asyncio.create_task(update_or_create_user_vocab(uv))
    return quiz

    
