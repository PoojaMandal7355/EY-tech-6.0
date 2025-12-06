# Docker Setup Guide for Windows

## Issue: Docker not recognized

Your system doesn't have Docker installed or it's not in your PATH.

## Solution 1: Install Docker Desktop (Recommended)

### Step 1: Download Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer

### Step 2: Install Docker Desktop
- Follow the installation wizard
- Accept all default settings
- Restart your computer when prompted
- Docker Desktop will start automatically

### Step 3: Verify Installation
```powershell
docker --version
docker compose version
```

### Step 4: Start Docker Services
```powershell
cd C:\Users\DELL\OneDrive\Documents\GitHub\PharmaPilot\backend
docker compose up -d
```

---

## Solution 2: Use Pre-built Database (No Docker Required)

If you don't want to install Docker, you can:

### Option A: Use PostgreSQL locally installed
1. Install PostgreSQL: https://www.postgresql.org/download/windows/
2. Create database and user
3. Update `.env` with your local PostgreSQL connection

### Option B: Use PostgreSQL cloud service
1. Create account on Render, Railway, or similar
2. Create free PostgreSQL database
3. Get connection string
4. Update `.env` DATABASE_URL

---

## Quick Docker Desktop Check

Is Docker Desktop currently installed?

```powershell
# Check in Programs
Get-WmiObject -Query "SELECT * FROM Win32_Product WHERE Name LIKE '%Docker%'"

# Or check registry
Test-Path "HKLM:\Software\Docker Inc"
```

## Troubleshooting

### Docker starts but containers fail
- Ensure Docker Desktop is fully started (wait 30 seconds)
- Check Docker Dashboard for errors
- Run: `docker system prune` to clean up

### Port 5432 already in use
- Change PORT in docker-compose.yml to 5433
- Update DATABASE_URL in .env

### Docker not starting on Windows
- Enable Hyper-V in Windows
- Or use Docker with WSL2 backend
- See: https://docs.docker.com/desktop/install/windows-install/
