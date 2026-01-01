from models.user_vocab import UserVocab

async def get_step_mark():
    pass 

async def should_change_step(uv:UserVocab, mark: float):
    step_change = 0
    step_mark, times = await get_step_mark()
    if uv.evaluate:
        if times > 8:
            if step_mark > 0.92:
                uv.evaluate_count += 1
                step_change = 3
            elif step_mark > 0.8:
                uv.evaluate_count += 1
                step_change = 1
            elif step_mark < 0.4:
                uv.evaluate_count = 0
                step_change = -1
    else:
        if times > 30:
            if step_mark > 0.7:
                step_change = 1
        elif times > 15:
            if step_mark > 0.9:
                step_change = 1