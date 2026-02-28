from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    quiz, results, stats,
    exercise,
    # auth,
    course
)
from utils.db import run_query


async def _run_migrations():
    migrations = [
        "CREATE SCHEMA IF NOT EXISTS users_data",
        """CREATE TABLE IF NOT EXISTS users_data.results (
            id SERIAL PRIMARY KEY,
            user_id varchar(100),
            lang varchar(12),
            to_lang varchar(12),
            course_id int8 DEFAULT 0,
            module_id int8 DEFAULT 0,
            lesson_id int8 DEFAULT 0,
            exercise_id int8 DEFAULT 0,
            exercise_type varchar(100) DEFAULT '',
            correct boolean DEFAULT false,
            attempts int DEFAULT 0,
            answer_delay_ms int DEFAULT 0,
            created_at timestamp DEFAULT now()
        )""",
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


app.include_router(quiz.router,
    prefix="/api/v1/quiz",
    tags=["quiz"])
app.include_router(results.router,
    prefix="/api/v1/results",
    tags=["results"])
app.include_router(stats.router,
    prefix="/api/v1/stats",
    tags=["stats"])

# app.include_router(auth.router,
#     prefix="/api/v1/auth",
#     tags=["auth"])

app.include_router(course.router,
    prefix="/api/v1/course",
    tags=["course"])
app.include_router(exercise.router,
    prefix="/api/v1/exercise",
    tags=["exercise"])
