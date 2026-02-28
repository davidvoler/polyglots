from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

#for running locally
# os.environ["POSTGRES_PORT"] = "5432"

from routers import (
    course,
    generate,
    words_select
)
from utils.db import run_query


async def _run_migrations():
    migrations = [
        "ALTER TABLE content.exercise ADD COLUMN IF NOT EXISTS audio_link varchar(300) DEFAULT ''",
    ]
    for sql in migrations:
        await run_query(sql, ())


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await _run_migrations()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


app.include_router(course.router, prefix="/api/v1/course", tags=["course"])
app.include_router(generate.router, prefix="/api/v1/generate", tags=["generate"])
app.include_router(words_select.router, prefix="/api/v1/words_select", tags=["words_select"])
