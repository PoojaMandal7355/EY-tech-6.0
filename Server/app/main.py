from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .config import settings
from .database import Base, engine
from .routes import auth, projects, chat
from starlette.middleware.base import BaseHTTPMiddleware


def create_tables_with_retry():
    max_retries = 5
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✓ Database initialized")
            return True
        except Exception:
            if i < max_retries - 1:
                import time
                time.sleep(2)
            else:
                return False
    return False


# Initialize database
try:
    create_tables_with_retry()
except Exception:
    pass

app = FastAPI(
    title="PharmaPilot API",
    description="Backend API for PharmaPilot - Pharmaceutical Research Platform",
    version="1.0.0"
)


# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                    "Access-Control-Allow-Headers": request.headers.get("access-control-request-headers", "*"),
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Max-Age": "3600"
                }
            )
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"  # Prevent MIME type sniffing
        response.headers["X-Frame-Options"] = "DENY"  # Prevent clickjacking
        response.headers["X-XSS-Protection"] = "1; mode=block"  # XSS protection
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"  # HSTS
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        return response


app.add_middleware(SecurityHeadersMiddleware)


# Configure CORS
origins = settings.cors_origins_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(projects.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "PharmaPilot API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "sqlite"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
