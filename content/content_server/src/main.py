from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os 

#for running locally
os.environ["POSTGRES_PORT"] = "5433"

from routers import (
    dashboard,
    review,
    course,
    translate,
    dialogues,
    subtitles,
    corpus,
    analyze_sentence,
    generate_content,
)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(corpus.router, prefix="/api/v1/corpus", tags=["corpus"])
app.include_router(review.router, prefix="/api/v1/review", tags=["review"])
app.include_router(analyze_sentence.router, prefix="/api/v1/analyze_sentence", tags=["analyze_sentence"])
app.include_router(generate_content.router, prefix="/api/v1/generate_content", tags=["generate_content"])
app.include_router(course.router, prefix="/api/v1/course", tags=["course"])
app.include_router(translate.router, prefix="/api/v1/translate", tags=["translate"])
app.include_router(dialogues.router, prefix="/api/v1/dialogues", tags=["dialogues"])
app.include_router(subtitles.router, prefix="/api/v1/subtitles", tags=["subtitles"])
