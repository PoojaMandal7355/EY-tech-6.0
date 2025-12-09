# ⚡ PharmaPilot Backend - Quick Reference

## 🚀 Start Backend (Choose One)

### Windows PowerShell
```powershell
cd backend
.\start.ps1
```

### Windows Command Prompt
```cmd
cd backend
start.bat
```

### Manual Start
```powershell
cd backend
.\venv\Scripts\Activate.ps1      # Activate venv
docker-compose up -d              # Start database
uvicorn app.main:app --reload    # Start API
```

---

## 📍 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API Base** | http://localhost:8000 | Backend API |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health** | http://localhost:8000/health | Health check |
| **Frontend** | http://localhost:5173 | React app (Vite) |

---

## 🔐 API Endpoints

### Authentication (`/api/v1/auth`)

```http
POST   /api/v1/auth/register      # Register new user
POST   /api/v1/auth/login         # Login (get tokens)
GET    /api/v1/auth/me            # Get current user (requires token)
POST   /api/v1/auth/refresh       # Refresh access token
POST   /api/v1/auth/forgot-password  # Request password reset
```

### Projects (`/api/v1/projects`)

```http
GET    /api/v1/projects           # List all projects
POST   /api/v1/projects           # Create project
GET    /api/v1/projects/{id}      # Get project
PUT    /api/v1/projects/{id}      # Update project
DELETE /api/v1/projects/{id}      # Delete project
```

### AI Agents (`/api/v1/agents`)

```http
POST   /api/v1/agents/execute     # Execute AI agent
GET    /api/v1/agents/logs        # Get agent logs
GET    /api/v1/agents/logs/{id}   # Get specific log
```

---

## 📝 Example Requests

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "password123",
    "role": "researcher"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Create Project (with token)
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Aspirin Research",
    "molecule_name": "Aspirin",
    "description": "Research project for aspirin"
  }'
```

### Execute Agent (with token)
```bash
curl -X POST http://localhost:8000/api/v1/agents/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "project_id": 1,
    "agent_type": "patent_search",
    "input_text": "Search for aspirin patents"
  }'
```

---

## 🗄️ Database

### Start/Stop Database
```bash
docker-compose up -d      # Start
docker-compose down       # Stop
docker-compose restart    # Restart
docker-compose logs -f    # View logs
```

### Reset Database (⚠️ Deletes all data)
```bash
docker-compose down -v
docker-compose up -d
```

### Connect to Database
```bash
docker exec -it pharmapilot_db psql -U postgres -d pharmapilot
```

---

## 🧪 Testing

### Run Test Suite
```bash
cd backend
.\venv\Scripts\Activate.ps1
pip install requests  # Install if not already
python test_backend.py
```

### Test Individual Endpoints
Use the interactive docs: http://localhost:8000/docs

---

## 🛠️ Common Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Virtual Environment
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## 🐛 Troubleshooting

### Port 8000 in use
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database connection failed
```bash
docker-compose down
docker-compose up -d
Start-Sleep -Seconds 10
```

### Module not found
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### PowerShell execution policy error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📂 File Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Settings
│   ├── database.py      # DB connection
│   ├── models.py        # Database models
│   ├── auth.py          # JWT authentication
│   └── routes/
│       ├── auth.py      # Auth endpoints
│       ├── projects.py  # Project endpoints
│       └── agents.py    # Agent endpoints
├── requirements.txt     # Python packages
├── docker-compose.yml   # PostgreSQL config
├── .env                 # Environment variables
└── README.md           # Documentation
```

---

## 🔑 Environment Variables

Edit `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/pharmapilot
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 📊 Database Schema

### Users Table
```sql
id, email, full_name, password, role, is_active, created_at, updated_at
```

### Projects Table
```sql
id, user_id, name, molecule_name, description, status, created_at, updated_at
```

### Agent Logs Table
```sql
id, project_id, agent_type, input_text, output_text, status, created_at
```

---

## 🎯 Daily Workflow

### Morning Setup
```bash
# Terminal 1: Backend
cd backend
.\venv\Scripts\Activate.ps1
docker-compose up -d
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd Client
npm run dev
```

### Evening Shutdown
```bash
# Stop backend: Ctrl+C in terminal
# Stop database: docker-compose down
# Stop frontend: Ctrl+C in terminal
```

---

## 💡 Tips

- ✅ Keep Docker Desktop running
- ✅ Always activate venv before running backend
- ✅ Use `/docs` for testing endpoints
- ✅ Check `backend/README.md` for detailed docs
- ✅ Frontend auto-connects to backend
- ✅ Tokens stored in localStorage by frontend

---

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **JWT Docs**: https://jwt.io/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## 🆘 Need Help?

1. Check `/docs` for API documentation
2. Read `SETUP.md` for setup instructions
3. Read `README.md` for detailed documentation
4. Read `COMPARISON.md` to understand the architecture

---

**Ready to build? Start the backend and start coding!** 🚀
