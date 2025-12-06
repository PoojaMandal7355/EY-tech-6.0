# PharmaPilot Backend - Complete Setup Guide

## Step-by-Step Setup Instructions

### Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9 or higher installed
- [ ] Docker Desktop installed and running
- [ ] Git installed
- [ ] Terminal/Command Prompt access

Verify Python version:
```bash
python --version  # Should be 3.9+
```

---

## Installation Steps

### Step 1: Navigate to Backend Directory

```bash
cd C:\Users\DELL\OneDrive\Documents\GitHub\PharmaPilot\backend
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (macOS/Linux)
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- SQLAlchemy (database ORM)
- asyncpg (async PostgreSQL driver)
- Pydantic (validation)
- python-jose (JWT)
- passlib/bcrypt (password hashing)
- And more...

### Step 4: Start Database & Cache with Docker

```bash
# Start PostgreSQL and Redis containers
docker-compose up -d

# Verify containers are running
docker-compose ps

# Output should show:
# NAME                COMMAND                  STATUS
# pharmapilot_postgres   "docker-entrypoint.s…"   Up (healthy)
# pharmapilot_redis      "redis-server"           Up (healthy)

# Wait for healthchecks to pass (about 10 seconds)
```

### Step 5: Verify Database Connection

```bash
# Test PostgreSQL connection
docker-compose exec postgres psql -U postgres -d pharmapilot -c "SELECT 1"

# Should output: 1
```

### Step 6: Run the Backend Server

```bash
# Start with hot reload (development)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Output should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started server process [12345]
# INFO:     Application startup complete
```

---

## Verification Checklist

### Check Server is Running

Open browser and visit:
- http://localhost:8000/health

Should return:
```json
{
  "status": "healthy",
  "app": "PharmaPilot"
}
```

### Access API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

You should see all API endpoints listed.

### Verify Database Created

Tables should auto-create on startup. Check:
```bash
docker-compose exec postgres psql -U postgres -d pharmapilot -c "\dt"

# Should show:
#            List of relations
# Schema |        Name        | Type  | Owner
#--------+--------------------+-------+----------
# public | users              | table | postgres
# public | projects           | table | postgres
# public | research_sessions  | table | postgres
# public | agent_requests     | table | postgres
# public | documents          | table | postgres
```

---

## Testing the API

### Test 1: Register User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "researcher@example.com",
    "password": "SecurePassword123",
    "full_name": "Dr. John Researcher",
    "role": "researcher"
  }'

# Response should include user ID and email
```

### Test 2: Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "researcher@example.com",
    "password": "SecurePassword123"
  }'

# Response should include:
# {
#   "access_token": "eyJhbGc...",
#   "refresh_token": "eyJhbGc...",
#   "token_type": "bearer"
# }

# COPY THE access_token VALUE - you'll need it for next steps
```

### Test 3: Get Current User (Protected Route)

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"

# Response should show your user details
```

### Test 4: Create Project

```bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin Research 2024",
    "description": "Analysis of aspirin efficacy",
    "molecule_name": "Acetylsalicylic acid",
    "indication": "Pain and inflammation",
    "status": "active"
  }'

# Response should include project ID
```

### Test 5: Use Interactive API Docs (Easiest)

1. Open http://localhost:8000/docs
2. Click the "Authorize" button (top right)
3. Fill in:
   - Username: (leave empty)
   - Password: (leave empty)
   - Click "Authorize"
4. Now try any endpoint by clicking "Try it out"

---

## Troubleshooting

### Problem: Port 8000 Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID 12345 /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Problem: PostgreSQL Won't Start

```
docker: Error response from daemon: driver failed programming external connectivity
```

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove volumes and restart
docker-compose down -v
docker-compose up -d

# Wait 15 seconds for initialization
```

### Problem: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Ensure venv is activated
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Problem: Database Tables Not Created

**Solution:**
Tables auto-create on app startup. Just restart the server:
```bash
# Kill server (Ctrl+C)
# Restart
python -m uvicorn app.main:app --reload
```

### Problem: Can't Connect to PostgreSQL

```
sqlalchemy.exc.OperationalError: could not translate host name
```

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart if needed
docker-compose restart postgres

# Wait 10 seconds for healthcheck
```

### Problem: CORS Error from Frontend

```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
Edit `.env`:
```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://your-frontend:port"]
```

Restart the server.

---

## Development Workflow

### Daily Startup

```bash
# 1. Navigate to backend
cd backend

# 2. Activate venv
venv\Scripts\activate

# 3. Start Docker services
docker-compose up -d

# 4. Start server (with auto-reload)
python -m uvicorn app.main:app --reload
```

### Making Changes

Since the server runs with `--reload`, changes auto-reload:
1. Edit Python file
2. Save file
3. Server automatically reloads
4. Test your changes

### Adding New Models

To add a new database model:

1. Create model file in `app/models/`
2. Inherit from `Base`
3. Define columns with proper types
4. Update `__init__.py` to export model
5. Restart server (tables auto-create)

Example:
```python
# app/models/experiment.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    # Add columns...
```

### Adding New API Endpoints

1. Create route file in `app/api/v1/`
2. Import router: `router = APIRouter(prefix="/api/v1/xyz", tags=["xyz"])`
3. Create endpoint functions with type hints
4. Import router in `app/main.py`: `app.include_router(xyz.router)`
5. Restart server

Example:
```python
@router.post("/xyz")
async def create_xyz(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Create something"""
    # Your code
    return {"result": "success"}
```

---

## Database Backup & Restore

### Backup Database

```bash
docker-compose exec postgres pg_dump -U postgres pharmapilot > backup.sql
```

### Restore Database

```bash
docker-compose exec postgres psql -U postgres pharmapilot < backup.sql
```

---

## Stopping Services

### Stop Everything Gracefully

```bash
# 1. Stop server (Ctrl+C in terminal)

# 2. Stop containers
docker-compose down

# 3. Deactivate venv
deactivate
```

### Remove All Data (WARNING)

```bash
# Delete database and redis data
docker-compose down -v

# This cannot be undone!
```

---

## Production Deployment

### Environment Setup

1. Create `.env.production`:
```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=USE_STRONG_RANDOM_KEY_HERE
DATABASE_URL=YOUR_PRODUCTION_DB_URL
REDIS_URL=YOUR_PRODUCTION_REDIS_URL
CORS_ORIGINS=["https://your-domain.com"]
```

2. Use strong SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Run with Gunicorn

```bash
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --env-file .env.production
```

### Docker Deployment

```bash
# Build image
docker build -t pharmapilot-backend .

# Run container
docker run -p 8000:8000 \
  --env-file .env.production \
  pharmapilot-backend
```

---

## Monitoring & Logs

### View Application Logs

```bash
# Real-time logs
docker-compose logs -f

# Specific service
docker-compose logs postgres
docker-compose logs redis
```

### Check Container Health

```bash
docker-compose ps

# Should show all containers "Up"
```

### Database Statistics

```bash
docker-compose exec postgres psql -U postgres -d pharmapilot

# In PostgreSQL shell:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM agent_requests;
\q  # Exit
```

---

## Next Steps

1. **Frontend Integration**
   - Configure CORS in `.env`
   - Update API base URL in frontend code
   - Test auth flow

2. **AI Agent Integration**
   - Agents call POST `/api/v1/agents/{type}/execute`
   - Backend stores request and returns request_id
   - Agents process and update results

3. **Additional Features**
   - Add email notifications
   - Implement Redis caching
   - Add request rate limiting
   - Set up webhooks for agents

4. **Testing**
   - Run unit tests: `pytest tests/`
   - Use `tests/test_api.py` as template
   - Test with `httpx` for async tests

5. **Documentation**
   - Keep API docs in `/docs`
   - Document agent integration spec
   - Create deployment guide

---

## Getting Help

### Check Logs for Errors

```bash
# Server logs (in terminal where it runs)
# Shows error messages and stack traces

# Docker logs
docker-compose logs
```

### Reset Everything

If something breaks, reset:
```bash
# Stop everything
docker-compose down -v

# Deactivate and reactivate venv
deactivate
venv\Scripts\activate

# Reinstall
pip install -r requirements.txt

# Restart
docker-compose up -d
python -m uvicorn app.main:app --reload
```

### Useful Resources

- API Docs: http://localhost:8000/docs
- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- PostgreSQL: https://www.postgresql.org/docs

---

**You're all set! Your PharmaPilot backend is ready for development! 🚀**
