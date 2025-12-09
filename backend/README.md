# 🚀 PharmaPilot Backend

**Simple, clean, production-ready FastAPI backend for pharmaceutical research.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 📚 Complete Documentation

| Document | Description |
|----------|-------------|
| **[SETUP.md](SETUP.md)** | 🔧 Complete setup instructions with screenshots |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | ⚡ Quick commands and API reference |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🎨 Visual system architecture diagrams |
| **[COMPARISON.md](COMPARISON.md)** | 📊 Why simple is better than complex |
| **[SUMMARY.md](SUMMARY.md)** | 🎉 Complete summary and next steps |

---

## ⚡ Quick Start (60 seconds)

```powershell
# Navigate to backend folder
cd backend

# Run the quick start script
.\start.ps1
```

That's it! Backend will start on **http://localhost:8000**

---

## ✅ What's Included

### 🔐 Authentication System
- ✅ User registration
- ✅ JWT-based login
- ✅ Token refresh
- ✅ Password reset (mock)
- ✅ Protected routes

### 📊 Project Management
- ✅ Create projects
- ✅ List all projects
- ✅ Update projects
- ✅ Delete projects
- ✅ User-specific data

### 🤖 AI Agent Interface
- ✅ Execute agents
- ✅ Store results
- ✅ View history
- ✅ Project-based tracking

### 🗄️ Database
- ✅ PostgreSQL (Docker)
- ✅ 3 tables (Users, Projects, AgentLogs)
- ✅ Automatic migrations
- ✅ Relationships configured

---

## 📊 Simple, clean FastAPI backend for PharmaPilot pharmaceutical research platform.

## 📁 File Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app (entry point)
│   ├── config.py        # Settings & configuration
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models (User, Project, AgentLog)
│   ├── auth.py          # JWT authentication logic
│   └── routes/
│       ├── auth.py      # Auth endpoints (register, login, me)
│       ├── projects.py  # Project CRUD endpoints
│       └── agents.py    # AI agent interface
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # PostgreSQL container
├── .env                 # Environment variables
└── README.md           # This file
```

## ⚡ Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Database

```bash
docker-compose up -d
```

### 3. Configure Environment

Edit `.env` file if needed (defaults work for local development).

### 4. Run Backend

```bash
# From backend directory
uvicorn app.main:app --reload --port 8000
```

Backend will be running at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

## 🔗 API Endpoints

### Authentication (`/api/v1/auth`)

- **POST** `/register` - Register new user
  ```json
  {
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "password123",
    "role": "researcher"
  }
  ```

- **POST** `/login` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
  Returns: `access_token`, `refresh_token`

- **GET** `/me` - Get current user info (requires auth)
- **POST** `/refresh` - Refresh access token
- **POST** `/forgot-password` - Request password reset

### Projects (`/api/v1/projects`)

- **GET** `/projects` - List all projects (requires auth)
- **POST** `/projects` - Create new project (requires auth)
- **GET** `/projects/{id}` - Get project by ID (requires auth)
- **PUT** `/projects/{id}` - Update project (requires auth)
- **DELETE** `/projects/{id}` - Delete project (requires auth)

### AI Agents (`/api/v1/agents`)

- **POST** `/agents/execute` - Execute AI agent (requires auth)
- **GET** `/agents/logs` - Get agent logs (requires auth)
- **GET** `/agents/logs/{id}` - Get specific log (requires auth)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

1. **Register** or **Login** to get tokens
2. Store `access_token` in your frontend
3. Include in requests: `Authorization: Bearer <access_token>`
4. Use `refresh_token` to get new `access_token` when expired

## 🗄️ Database Tables

### Users
- `id`, `email`, `full_name`, `password`, `role`, `is_active`
- `created_at`, `updated_at`

### Projects
- `id`, `user_id`, `name`, `molecule_name`, `description`, `status`
- `created_at`, `updated_at`

### Agent Logs
- `id`, `project_id`, `agent_type`, `input_text`, `output_text`, `status`
- `created_at`

## 🛠️ Development

### Check API Docs
Visit http://localhost:8000/docs for interactive API documentation.

### Database Commands

```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down

# View logs
docker-compose logs -f

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 🔄 Frontend Integration

Your React frontend is configured to connect to this backend at:
```
http://localhost:8000/api/v1
```

Make sure the backend is running before starting your frontend.

## 📦 Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Uvicorn** - ASGI server
- **Docker** - Database containerization

## 🚨 Troubleshooting

### Port 8000 already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Database connection error
```bash
# Check if PostgreSQL is running
docker ps

# Restart database
docker-compose restart
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 🎯 Production Deployment

Before deploying to production:

1. Change `SECRET_KEY` in `.env` to a secure random string
2. Update `CORS_ORIGINS` to include your frontend domain
3. Use a managed PostgreSQL database (not Docker)
4. Enable HTTPS
5. Set up proper logging and monitoring

## 📝 Notes

- Database tables are created automatically on startup
- CORS is configured for `localhost:3000` and `localhost:5173` (Vite)
- Password reset currently returns mock response (implement email in production)
- All endpoints return JSON
- Errors follow HTTP status code conventions

## 🤝 For AI Agent Developers

To integrate your AI agents:

1. User creates a project via `/api/v1/projects`
2. Your agent calls `/api/v1/agents/execute` with:
   - `project_id`
   - `agent_type` (e.g., "patent_search", "clinical_trial")
   - `input_text` (user query)
3. Store results in the response
4. View execution history at `/api/v1/agents/logs`

---

Built with ❤️ for PharmaPilot
