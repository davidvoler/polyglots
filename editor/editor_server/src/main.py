from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os 

#for running locally
os.environ["POSTGRES_PORT"] = "5433"

from routers import (
    course,
    generate,
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


app.include_router(course.router, prefix="/api/v1/course", tags=["course"])
app.include_router(generate.router, prefix="/api/v1/generate", tags=["generate"])
