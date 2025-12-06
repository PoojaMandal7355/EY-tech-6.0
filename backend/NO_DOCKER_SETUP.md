# PharmaPilot Backend - Running Without Docker

Since Docker isn't available on your system, here are your options:

## Option 1: Using PostgreSQL locally (Easiest)

### Step 1: Install PostgreSQL
1. Download: https://www.postgresql.org/download/windows/
2. Run installer
3. Remember the password you set for `postgres` user
4. Accept default port 5432

### Step 2: Create Database
```sql
-- Open pgAdmin (comes with PostgreSQL) or run psql:
psql -U postgres

-- In psql prompt, run:
CREATE DATABASE pharmapilot;
CREATE USER pharmapilot WITH PASSWORD 'pharmapilot_password';
ALTER ROLE pharmapilot SET client_encoding TO 'utf8';
ALTER ROLE pharmapilot SET default_transaction_isolation TO 'read committed';
ALTER ROLE pharmapilot SET default_transaction_deferrable TO on;
ALTER ROLE pharmapilot SET default_transaction_deferrable TO on;
ALTER ROLE pharmapilot SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pharmapilot TO pharmapilot;
```

### Step 3: Update .env
```env
DATABASE_URL=postgresql+asyncpg://pharmapilot:pharmapilot_password@localhost:5432/pharmapilot
DATABASE_SYNC_URL=postgresql://pharmapilot:pharmapilot_password@localhost:5432/pharmapilot
REDIS_URL=redis://localhost:6379/0  # Set to empty if Redis not available
```

### Step 4: Initialize Database
```powershell
python init_db.py
```

### Step 5: Start Backend
```powershell
python -m uvicorn app.main:app --reload
```

---

## Option 2: Using PostgreSQL Cloud Service (No installation needed)

### Recommended Services (Free tier available):
- **Render**: https://render.com (Recommended - easiest)
- **Railway**: https://railway.app
- **Supabase**: https://supabase.com
- **ElephantSQL**: https://www.elephantsql.com

### Example with Render:

1. Go to https://render.com
2. Sign up (free account)
3. Create new PostgreSQL database
4. Get connection string: `postgresql://...`
5. Update `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
DATABASE_SYNC_URL=postgresql://user:password@host:5432/dbname
```
6. Run: `python init_db.py`
7. Start backend: `python -m uvicorn app.main:app --reload`

---

## Option 3: Using SQLite (Development Only)

Not recommended for production, but good for testing:

### Update core/config.py:
```python
# Change from PostgreSQL to SQLite
if self.environment == "development":
    database_url: str = "sqlite+aiosqlite:///./test.db"
else:
    database_url: str = "postgresql+asyncpg://..."
```

---

## Option 4: Docker - Installation Steps

If you want to use Docker later:

### Install Docker Desktop:
1. https://www.docker.com/products/docker-desktop
2. Run installer
3. Restart computer
4. Run: `docker compose up -d`

---

## Disable Redis (Optional)

If you don't have Redis, the app will work fine without it:

### Update services if needed:
- Redis is optional - system works without it
- If you get Redis connection errors, it's safe to ignore them for development

---

## Recommended: PostgreSQL Local Installation

**Pros:**
- ✅ Easiest to setup
- ✅ Works immediately
- ✅ No cloud accounts needed
- ✅ Full control of data
- ✅ Good for development

**Steps:**
1. Install PostgreSQL (Windows installer): https://www.postgresql.org/download/windows/
2. Create database using pgAdmin or psql
3. Update `.env` file
4. Run: `python init_db.py`
5. Run: `python -m uvicorn app.main:app --reload`

Done! ✅

---

## Testing Without Docker

Once database is setup, test the backend:

```powershell
# Terminal 1: Start backend
python -m uvicorn app.main:app --reload

# Terminal 2: Test endpoints
Invoke-WebRequest http://localhost:8000/health

# Or open browser: http://localhost:8000/docs
```

---

## Still Want Docker?

```powershell
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop

# Then run:
docker compose up -d

# Start backend:
python -m uvicorn app.main:app --reload
```

---

**Which option do you prefer?**
1. Local PostgreSQL (recommended for development)
2. Cloud PostgreSQL (Render/Railway)
3. Docker (after installation)

Let me know if you need help with any of these!
