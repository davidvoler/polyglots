from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    quiz, results, stats, 
    # auth,
    course
)


# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "http://localhost:3000",
#     "http://localhost:3001",
#     "http://127.0.0.1:3000",
#     "http://127.0.0.1:3001",
#     "http://127.0.0.1:*",
#     "http://localhost:5000",
#     "http://10.0.2.2:8000",
#     "http://172.18.0.1:8000",
#     "http://172.18.0.1:8080",
#     "http://172.18.0.1:*",
#     "http://localhost:*",
#     "http://0.0.0.0:*",
#     "http://0.0.0.0",
#     "*",
# ]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
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

