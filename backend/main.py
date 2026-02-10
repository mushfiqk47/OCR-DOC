from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import ocr, translate, table, conversion
from backend.config import settings
import uvicorn
import os

app = FastAPI(
    title="DocIntel — Document Intelligence Platform",
    description="Enterprise-grade API for high-fidelity OCR, massive table extraction, and layout-preserving translation. Supports 20+ document intelligence services.",
    version="2.0.0"
)

# File size limit middleware (50MB)
MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024

@app.middleware("http")
async def file_size_limit(request: Request, call_next):
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length:
            if int(content_length) > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB")
    response = await call_next(request)
    return response

# CORS Middleware
# Allow all origins for development convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(ocr.router)
app.include_router(translate.router)
app.include_router(table.router)
app.include_router(conversion.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": settings.OCR_MODEL}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
