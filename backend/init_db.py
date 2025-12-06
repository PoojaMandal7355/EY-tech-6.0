"""
Database initialization script - for running without Docker
Run this script to create database tables without Docker containers
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import init_db, engine
from app.core.config import settings


async def initialize_database():
    """Initialize database tables"""
    try:
        print("=" * 60)
        print("PharmaPilot Backend - Database Initialization")
        print("=" * 60)
        print()
        
        print(f"📦 Database: {settings.database_url}")
        print(f"🔧 Environment: {settings.environment}")
        print()
        
        print("⏳ Creating database tables...")
        await init_db()
        print("✅ Database tables created successfully!")
        print()
        
        print("📋 Database is ready for use")
        print()
        print("Next steps:")
        print("1. Start the backend: python -m uvicorn app.main:app --reload")
        print("2. Open API docs: http://localhost:8000/docs")
        print("3. Register a user: POST /api/v1/auth/register")
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}", file=sys.stderr)
        print()
        print("Troubleshooting:")
        print("1. Check DATABASE_URL in .env file")
        print("2. Ensure PostgreSQL is running")
        print("3. Verify database credentials")
        raise


if __name__ == "__main__":
    asyncio.run(initialize_database())
