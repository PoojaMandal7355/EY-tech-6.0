"""
PharmaPilot Backend - FastAPI Application
Simple, clean backend for pharmaceutical research platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routes import auth, projects, agents
import time

# Create database tables (with retry logic)
def create_tables_with_retry():
    max_retries = 5
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully!")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"⏳ Waiting for database to be ready... (attempt {i+1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"⚠️  Could not connect to database. Make sure PostgreSQL is running.")
                print(f"   Run: docker-compose up -d")

create_tables_with_retry()

# Initialize FastAPI app
app = FastAPI(
    title="PharmaPilot API",
    description="Backend API for PharmaPilot - Pharmaceutical Research Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(projects.router, prefix=settings.API_V1_PREFIX)
app.include_router(agents.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PharmaPilot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
