# PharmaPilot Backend - Setup Complete ✅

## Current Status

✅ **Python Dependencies**: Installed and verified
✅ **Configuration**: Loaded successfully  
✅ **Code Structure**: Complete and ready
⏳ **Database**: Needs setup (choose one option below)

---

## Quick Start - Choose Your Database Setup

### 🟢 RECOMMENDED: Local PostgreSQL Installation

**Time:** ~10 minutes  
**Difficulty:** Easy

```powershell
# 1. Download & Install PostgreSQL
# https://www.postgresql.org/download/windows/

# 2. After installation, open Command Prompt as Admin:
psql -U postgres

# 3. In psql, create database:
CREATE DATABASE pharmapilot;
CREATE USER pharmapilot WITH PASSWORD 'pharmapilot_password';
GRANT ALL PRIVILEGES ON DATABASE pharmapilot TO pharmapilot;
\q

# 4. Update .env (already configured, just verify):
# DATABASE_URL=postgresql+asyncpg://pharmapilot:pharmapilot_password@localhost:5432/pharmapilot

# 5. Initialize database tables:
python init_db.py

# 6. Start backend:
python -m uvicorn app.main:app --reload

# 7. Open browser: http://localhost:8000/docs
```

---

### 🟡 ALTERNATIVE: Cloud Database (No Installation)

**Time:** ~5 minutes  
**Services:** Render, Railway, Supabase (all free tier available)

```powershell
# 1. Go to https://render.com (or Railway.app)
# 2. Create free PostgreSQL instance
# 3. Copy connection string
# 4. Update .env:
#    DATABASE_URL=postgresql+asyncpg://user:pass@host/db
#    DATABASE_SYNC_URL=postgresql://user:pass@host/db

# 5. Initialize database:
python init_db.py

# 6. Start backend:
python -m uvicorn app.main:app --reload
```

---

### 🔵 DOCKER: After Installation

**Time:** ~20 minutes (includes Docker install)

```powershell
# 1. Install Docker Desktop:
# https://www.docker.com/products/docker-desktop

# 2. Restart computer (Docker needs it)

# 3. Start containers:
docker compose up -d

# 4. Verify containers running:
docker compose ps

# 5. Initialize database:
python init_db.py

# 6. Start backend:
python -m uvicorn app.main:app --reload
```

---

## Database Setup Scripts

### Script 1: Auto Initialize (init_db.py)
```bash
python init_db.py
```
This creates all database tables automatically.

### Script 2: Test Database Connection
```bash
python -c "from app.core.database import get_db_session; print('✅ Database ready')"
```

### Script 3: Reset Database (Caution!)
```bash
python -c "
import asyncio
from app.core.database import engine, Base

async def reset():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Database reset')

asyncio.run(reset())
"
```

---

## Environment Variables

All configured in `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/pharmapilot
DATABASE_SYNC_URL=postgresql://user:pass@localhost:5432/pharmapilot

# Redis (optional, can leave as is)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=pharma-pilot-secret-key-change-in-production-32-chars-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_NAME=PharmaPilot
DEBUG=True
PORT=8000

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# File uploads
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads
```

---

## Testing Endpoints

### After Backend Starts (http://localhost:8000):

**Interactive API Documentation:**
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

**Health Check:**
```powershell
Invoke-WebRequest http://localhost:8000/health
```

**Register User:**
```powershell
$body = @{
    email = "test@example.com"
    password = "TestPassword123"
    full_name = "Test User"
    role = "researcher"
} | ConvertTo-Json

Invoke-WebRequest -Method POST `
    -Uri "http://localhost:8000/api/v1/auth/register" `
    -ContentType "application/json" `
    -Body $body
```

**Login:**
```powershell
$body = @{
    email = "test@example.com"
    password = "TestPassword123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Method POST `
    -Uri "http://localhost:8000/api/v1/auth/login" `
    -ContentType "application/json" `
    -Body $body

$response.Content | ConvertFrom-Json | Select-Object access_token
```

---

## Project Files Summary

```
backend/
├── app/
│   ├── main.py                    # FastAPI app
│   ├── core/
│   │   ├── config.py              # Settings
│   │   ├── database.py            # Database setup
│   │   ├── security.py            # JWT & password
│   │   └── deps.py                # Dependencies
│   ├── models/                    # Database models
│   │   ├── user.py, project.py, agent.py, document.py
│   ├── schemas/                   # Pydantic schemas
│   │   ├── user.py, project.py, agent.py, document.py
│   ├── api/v1/                    # API routes
│   │   ├── auth.py, projects.py, agents.py, documents.py
│   ├── services/                  # Business logic
│   │   ├── auth_service.py, project_service.py, agent_service.py
│   └── utils/
│       └── file_handler.py        # File upload utility
├── tests/                         # Unit tests
├── uploads/                       # File storage
├── requirements.txt               # Python packages
├── docker-compose.yml             # Docker configuration
├── .env                           # Environment variables
├── .gitignore                     # Git config
├── init_db.py                     # Database initialization
├── DOCKER_SETUP.md                # Docker guide
├── NO_DOCKER_SETUP.md             # Non-Docker guide
├── SETUP_GUIDE.md                 # Complete setup guide
├── README.md                      # Main documentation
└── SETUP_GUIDE.md                 # Detailed setup steps
```

---

## Next Steps

### ✅ Already Done:
- ✅ All Python code written
- ✅ All dependencies installed
- ✅ Configuration ready
- ✅ API routes defined
- ✅ Database models created

### 🔄 Choose ONE database setup option above:
1. **Local PostgreSQL** (Recommended)
2. **Cloud Database** (Render/Railway)
3. **Docker** (After installation)

### 🚀 Then Run:
```powershell
# 1. Initialize database
python init_db.py

# 2. Start backend
python -m uvicorn app.main:app --reload

# 3. Open http://localhost:8000/docs

# 4. Test API with Swagger UI
```

---

## Troubleshooting

### "ModuleNotFoundError"
```powershell
# Activate venv and reinstall
venv\Scripts\activate
pip install -r requirements.txt
```

### "Database connection failed"
```powershell
# Check DATABASE_URL in .env
# Make sure PostgreSQL is running
# Test connection: python init_db.py
```

### "Port 8000 already in use"
```powershell
# Use different port
python -m uvicorn app.main:app --reload --port 8001
```

### "Docker not found"
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Or use PostgreSQL locally instead

---

## Recommended Setup Path

For fastest setup on Windows without Docker:

```powershell
# 1. Install PostgreSQL (10 minutes)
# 2. Create database (2 minutes)
# 3. python init_db.py (30 seconds)
# 4. python -m uvicorn app.main:app --reload (30 seconds)
# 5. Open http://localhost:8000/docs
```

**Total Time: ~15 minutes**

---

## Support Files Created

- `NO_DOCKER_SETUP.md` - Detailed non-Docker setup
- `DOCKER_SETUP.md` - Docker installation & troubleshooting
- `SETUP_GUIDE.md` - Complete step-by-step guide
- `init_db.py` - Database initialization script
- `README.md` - API documentation

---

## Ready? Let's Go! 🚀

**Pick your database option above and let me know if you hit any issues!**

For **Local PostgreSQL** (recommended):
1. Install PostgreSQL
2. Run the SQL commands in the "Local PostgreSQL" section
3. `python init_db.py`
4. `python -m uvicorn app.main:app --reload`

Done!
