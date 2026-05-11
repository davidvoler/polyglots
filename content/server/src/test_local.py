# from batch_tools.analyze_sentence.analyzer import analyze_sentence_with_translit

from batch_tools.analyze_sentence.analyzer_simple import analyze_sentence_batch
from batch_tools.collect_words.collect_words import collect_words, collect_words_pos, collect_words_pos1
from batch_tools.alphabet.ja import collect_words
import os 
import asyncio
from multiprocessing import Pool



os.environ['POSTGRES_PORT'] = '5432'


def anlyze_sentence_batch_wrapper(args):
    lang, limit, offset = args
    asyncio.run(analyze_sentence_batch(lang, limit, offset))

def main_mp():
    limit = 10000
    pool = Pool(processes=10)
    tasks = []
    for i in range(10):
            tasks.append(('ar', limit, limit*i))
    pool.map(anlyze_sentence_batch_wrapper, tasks)

async def main():
    tasks = []
    for i in range (10):
        tasks.append(analyze_sentence_batch( 'ar', limit=10000, offset=10000*i))
    await asyncio.gather(*tasks)
if __name__ == "__main__":
    asyncio.run(main_mp())
