from generators.generate_en import gen_course
import os
import asyncio


os.environ["POSTGRES_PORT"] = "5433"

asyncio.run(gen_course('en'))