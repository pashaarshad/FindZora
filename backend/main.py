import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.connection import engine, Base
from backend.api.events import router as events_router
from backend.api.photos import router as photos_router
from backend.api.search import router as search_router, universal_router
from backend.api.admin import router as admin_router

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FindZora API",
    description="Privacy-conscious AI-powered event photo discovery platform backend.",
    version="2.0.0"
)

# CORS configuration for Next.js & React.js frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(events_router)
app.include_router(photos_router)
app.include_router(search_router)
app.include_router(universal_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {
        "platform": "FindZora",
        "description": "AI-Powered Event Photo Discovery Platform",
        "version": "2.0.0",
        "docs_url": "/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
