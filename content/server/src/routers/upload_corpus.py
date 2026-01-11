"""
Upload corpus file to the server.
Implement:
- file processing 
- preview uploaded data
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from models.corpus import FileUploadResponse
import os

app = FastAPI()

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["text/plain", "application/json", "text/csv"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Validate file size (max 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    
    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }