from batch_tools.analyze_sentence.analyzer import analyze_sentence_with_translit
import asyncio

async def main():
    await analyze_sentence_with_translit('ja')

if __name__ == "__main__":
    asyncio.run(main())
