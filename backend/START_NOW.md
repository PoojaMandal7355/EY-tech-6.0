# ⚡ QUICK START - RUN THESE COMMANDS NOW

## Open PowerShell in backend folder and run these commands ONE BY ONE:

```powershell
# 1. Navigate to backend (if not already there)
cd C:\Users\Vighnesh\OneDrive\Documents\GitHub\EY-tech-6.0\backend

# 2. Create virtual environment (skip if exists)
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start PostgreSQL database in background
docker-compose up -d

# 6. Wait 10 seconds for database to start
timeout /t 10

# 7. Start the backend server
uvicorn app.main:app --reload --port 8000
```

## ✅ After running command #7, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 Then open your browser:

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🎉 SUCCESS!

Your backend is now running!

### Next Steps:

1. Open new terminal for frontend:
   ```powershell
   cd C:\Users\Vighnesh\OneDrive\Documents\GitHub\EY-tech-6.0\Client
   npm install
   npm run dev
   ```

2. Test the backend:
   - Open http://localhost:8000/docs
   - Try the health endpoint
   - Try registering a user

3. Test with frontend:
   - Open http://localhost:5173
   - Register an account
   - Login

---

## 🚨 If you get errors:

**"Execution policy" error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Port 8000 in use:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database connection failed:**
```powershell
docker-compose down
docker-compose up -d
timeout /t 10
```

---

## 📝 TO STOP:

- Backend: Press `Ctrl+C` in the terminal
- Database: `docker-compose down`

---

**YOU HAVE EVERYTHING! JUST RUN THE COMMANDS ABOVE!** 🚀
