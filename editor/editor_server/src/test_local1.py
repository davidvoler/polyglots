from generators.module_words import get_words_pos, get_words_pos_rare
from generators.lessons_from_words import (load_words, create_greeting_lessons, 
load_words_no_duplicate, alphabet_by_words,
gen_description_lessons)
import asyncio
import os
from generators.course_from_sentences import sentences_from_folder, create_modules,correct_greeting
from generators.create_course_from_file import create_course_from_file, load_all_alphabet_exercises
from generators.complete_exercise import complete_exercise


os.environ["POSTGRES_PORT"] = "5433"  



async def get_words():
    words = await get_words_pos('ja')
    with open('../courses/japanese_english/words.csv', 'w') as f:
        for w in words:
            f.write(f"""{w.lang}\t{w.word}\t{w.pos}\t{w.min_wcount}\t{w.max_wcount}\t{w.sentences_count}\t{w.root_count}\n""")
        
async def get_words_rate():
    words = await get_words_pos_rare('ja')
    with open('../courses/japanese_english/words_rare.csv', 'w') as f:
        for w in words:
            f.write(f"""{w.lang}\t{w.word}\t{w.pos}\t{w.min_wcount}\t{w.max_wcount}\t{w.sentences_count}\t{w.root_count}\n""")

if __name__ == '__main__':
    # asyncio.run(get_words())
    # asyncio.run(load_words_no_duplicate("../courses/japanese_english/words_reviewd.csv","../courses/japanese_hebrew/course_no_duplicates.csv", 'ja','he'))
    #asyncio.run(load_words_no_duplicate("../courses/japanese_english/words_rare.csv","../courses/japanese_english/rare_duplicates.csv", 'ja','en'))
    # asyncio.run(alphabet_by_words("../courses/japanese_english/words_reviewd.csv","../courses/japanese_english/alphabet.csv", 'ja','en'))
    # asyncio.run(gen_description_lessons("../courses/japanese_english/description_lessons.csv"))
    # asyncio.run(get_words_rate())
    
    # asyncio.run(create_greeting_lessons("../courses/japanese_hebrew/", 'ja','he'))
    # sentences_from_folder('../courses/japanese_english/edited','../courses/japanese_english/edited/course.csv')
    # create_modules('../courses/japanese_english/edited')
    # asyncio.run(correct_greeting('../courses/japanese_english/edited'))
    # asyncio.run(test_insert_get_id())
    #asyncio.run(create_course_from_file('../courses/japanese_english/edited','ja','en', "Japanese course", "Japanese course" ))
    # asyncio.run(complete_exercise('ja','en'))
    asyncio.run(load_all_alphabet_exercises('../courses/japanese_english/edited','ja','en'))