"""
Main Application Entry
----------------------
Initializes FastAPI app
Configures CORS
Includes API routes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router


app = FastAPI(
    title="AI Crawler Intelligence Engine",
    description="Behavioral AI Crawler Detection & Scoring API",
    version="1.0.0"
)


# ==========================
# CORS Configuration
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# Include Routes
# ==========================

app.include_router(router)


# ==========================
# Health Check
# ==========================

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "AI Crawler Intelligence Engine"
    }
