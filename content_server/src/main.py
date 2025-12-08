from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    load_csv,
    analyze_sentence,
    transliterate,
    review,
    stats,
    auth,
    quiz,
    results,
    preview,
    tatoeba,
    lang_info,
    language,
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



app.include_router(load_csv.router, prefix="/api/load_csv")
app.include_router(analyze_sentence.router, prefix="/api/analyze_sentence")
app.include_router(transliterate.router, prefix="/api/transliterate")
app.include_router(review.router, prefix="/api/review")
app.include_router(stats.router, prefix="/api/stats")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(quiz.router, prefix="/api/quiz")
app.include_router(results.router, prefix="/api/results")
app.include_router(preview.router, prefix="/api/preview")
app.include_router(tatoeba.router, prefix="/api/tatoeba")
app.include_router(lang_info.router, prefix="/api/lang_info")
app.include_router(language.router, prefix="/api/language")