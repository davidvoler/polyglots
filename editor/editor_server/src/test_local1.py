from generators.module_words import get_words_pos
from generators.lessons_from_words import load_words, create_greeting_lessons
import asyncio
import os

os.environ["POSTGRES_PORT"] = "5433"  



async def get_words():
    words = await get_words_pos('ja')
    with open('../courses/japanese_english/words.csv', 'w') as f:
        for w in words:
            f.write(f"""{w.lang}\t{w.word}\t{w.pos}\t{w.min_wcount}\t{w.max_wcount}\t{w.sentences_count}\t{w.root_count}\n""")
        



if __name__ == '__main__':
    # asyncio.run(get_words())
    # asyncio.run(load_words("../courses/japanese_english/words_reviewd.csv","../courses/japanese_hebrew/course.csv", 'ja','he'))
    asyncio.run(create_greeting_lessons("../courses/japanese_hebrew/", 'ja','he'))