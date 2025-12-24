# from batch_tools.analyze_sentence.analyzer import analyze_sentence_with_translit
from batch_tools.collect_words.collect_words import collect_words, collect_words_pos
import os 
import asyncio

os.environ['POSTGRES_PORT'] = '5433'

async def main():
    await collect_words_pos('ja')

if __name__ == "__main__":
    asyncio.run(main())
