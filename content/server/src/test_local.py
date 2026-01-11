# from batch_tools.analyze_sentence.analyzer import analyze_sentence_with_translit
from batch_tools.collect_words.collect_words import collect_words, collect_words_pos, collect_words_pos1
from batch_tools.alphabet.ja import collect_words
import os 
import asyncio

os.environ['POSTGRES_PORT'] = '5433'

async def main():
    await collect_words_pos1('en')

if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(collect_words())
