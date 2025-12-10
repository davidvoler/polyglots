from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    dashboard,
    review,
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



app.include_router(dashboard.router, prefix="/api/dashboard")
app.include_router(review.router, prefix="/api/review")