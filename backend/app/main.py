"""FastAPI main application factory"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import auth, projects, agents, documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage FastAPI app lifecycle.
    Handles startup and shutdown events.
    """
    # Startup
    print(f"Starting {settings.app_name}...")
    await init_db()
    print("Database initialized")
    
    yield
    
    # Shutdown
    print(f"Shutting down {settings.app_name}...")
    await close_db()
    print("Database closed")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        description="Backend API for pharmaceutical research platform",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(auth.router)
    app.include_router(projects.router)
    app.include_router(agents.router)
    app.include_router(documents.router)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "app": settings.app_name,
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
