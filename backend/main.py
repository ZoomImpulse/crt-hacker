"""
CRT Hacker Game - Main Application Entry Point
FastAPI backend with WebSocket support
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.api.websocket import router as ws_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup, cleanup on shutdown"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="CRT Hacker Terminal Game",
    description="Backend API for terminal-based hacking game",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for development and Codespaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"https://.*\.github\.dev(:\d+)?",
)

# Include routers
app.include_router(ws_router, prefix="/ws", tags=["websocket"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "game": "CRT Hacker Terminal"}


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
