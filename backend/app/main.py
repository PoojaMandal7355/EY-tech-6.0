from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routes import auth, projects, agents
import time


def create_tables_with_retry():
    max_retries = 5
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database tables initialized successfully")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Waiting for database connection... (attempt {i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("Database connection failed. Ensure PostgreSQL is running.")
                raise



create_tables_with_retry()

app = FastAPI(
    title="PharmaPilot API",
    description="Backend API for PharmaPilot - Pharmaceutical Research Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(projects.router, prefix=settings.API_V1_PREFIX)
app.include_router(agents.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "PharmaPilot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
