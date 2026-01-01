from generators.gen_alphabet_exercise import get_words_so_far_for_exercise, get_extended, gen_alphabet_exercise,fix_alphabet_exercise
import os 
import asyncio
os.environ["POSTGRES_PORT"] = "5433"  



if __name__ == '__main__':
    # get_words_so_far_for_exercise('../courses/japanese_english/edited')
    # get_extended('../courses/japanese_english/edited')
    asyncio.run(fix_alphabet_exercise('ja', 'en'))
