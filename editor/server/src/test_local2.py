from generators.gen_alphabet_exercise import get_words_so_far_for_exercise, get_extended, gen_alphabet_exercise,fix_alphabet_exercise
import os 
import asyncio
from generators.exctract_aux import (
    extract_aux, 
    identify_words, 
    letter_in_words,
    )
from question_types.gen_from_course import gen_from_course
from question_types.create_course_from_file import create_course_from_file
os.environ["POSTGRES_PORT"] = "5433"  



if __name__ == '__main__':
    # get_words_so_far_for_exercise('../courses/japanese_english/edited')
    # get_extended('../courses/japanese_english/edited')
    # asyncio.run(fix_alphabet_exercise('ja', 'en'))
    # asyncio.run(extract_aux())
    # asyncio.run(identify_words(22554842))
    # asyncio.run(letter_in_words())
    asyncio.run(create_course_from_file('../courses/japanese_english/edited', 'ja', 'en', 'Japanese English', 'Japanese English'))