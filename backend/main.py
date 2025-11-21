# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

from dotenv import load_dotenv
import os

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine, Base
from routers import auth, profile, calculations


SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="ICMR Nutrition Planner API", version="1.0.0")

# # CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(calculations.router)
app.include_router(calculations.calculate_router)

# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@app.get("/")
def root():
    return {
        "message": "ICMR Nutrition Planner API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
