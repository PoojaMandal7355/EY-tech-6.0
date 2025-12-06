# PharmaPilot Backend

FastAPI backend for the PharmaPilot pharmaceutical research platform. Provides REST APIs for managing research projects, executing AI agents, and handling document uploads.

## Features

- ✅ **Async FastAPI** - High-performance async web framework
- ✅ **PostgreSQL** - Reliable relational database with SQLAlchemy 2.0
- ✅ **Redis** - Caching and session management
- ✅ **JWT Authentication** - Secure token-based auth with refresh tokens
- ✅ **Role-Based Access Control** - User roles and authorization
- ✅ **AI Agent Interface** - Support for 8 different AI agent types
- ✅ **File Upload Handling** - Document management with size limits
- ✅ **Auto API Docs** - Interactive API documentation at `/docs`
- ✅ **CORS Enabled** - Frontend integration ready
- ✅ **Docker Support** - Ready for containerization

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application factory
│   ├── core/
│   │   ├── config.py          # Settings management
│   │   ├── database.py        # Database connection & sessions
│   │   ├── security.py        # JWT & password hashing
│   │   └── deps.py            # Dependency injection
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── project.py         # Project & ResearchSession models
│   │   ├── agent.py           # AgentRequest model & AgentType enum
│   │   └── document.py        # Document model
│   ├── schemas/
│   │   ├── user.py            # User Pydantic schemas
│   │   ├── project.py         # Project Pydantic schemas
│   │   ├── agent.py           # Agent Pydantic schemas
│   │   └── document.py        # Document Pydantic schemas
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py        # Auth endpoints
│   │       ├── projects.py    # Project endpoints
│   │       ├── agents.py      # Agent endpoints
│   │       └── documents.py   # Document endpoints
│   ├── services/
│   │   ├── auth_service.py    # Auth business logic
│   │   ├── project_service.py # Project business logic
│   │   └── agent_service.py   # Agent business logic
│   └── utils/
│       └── file_handler.py    # File upload utilities
├── tests/                      # Unit tests
├── uploads/                    # Document storage
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker services (PostgreSQL, Redis)
├── .env                       # Environment variables
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Database**: PostgreSQL 16 + SQLAlchemy 2.0 + asyncpg
- **Cache**: Redis 7
- **Authentication**: python-jose (JWT) + passlib (bcrypt)
- **Validation**: Pydantic V2
- **File Handling**: python-multipart + aiofiles

## Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git

## Quick Start

### 1. Setup Environment

```bash
# Clone repository
cd PharmaPilot/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Database & Cache

```bash
# Start PostgreSQL and Redis containers
docker-compose up -d

# Verify containers are running
docker-compose ps

# Wait for healthchecks (approximately 10 seconds)
```

### 3. Initialize Database

```bash
# Database tables will auto-initialize on app startup
# No manual migration needed!
```

### 4. Run the Backend

```bash
# Start development server (with hot reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python app/main.py
```

Server will be available at `http://localhost:8000`

### 5. Access API Documentation

Open in your browser:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication (`/api/v1/auth`)

```bash
# Register user
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "researcher@example.com",
  "password": "SecurePassword123",
  "full_name": "Dr. John Researcher",
  "role": "researcher"
}

Response: { "id": 1, "email": "...", ... }


# Login
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "researcher@example.com",
  "password": "SecurePassword123"
}

Response: {
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}


# Get current user
GET /api/v1/auth/me
Authorization: Bearer {access_token}

Response: { "id": 1, "email": "...", ... }


# Refresh access token
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}

Response: { "access_token": "...", ... }
```

### Projects (`/api/v1/projects`)

```bash
# Create project
POST /api/v1/projects
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Aspirin Research 2024",
  "description": "Analysis of aspirin efficacy",
  "molecule_name": "Acetylsalicylic acid",
  "indication": "Pain and inflammation",
  "status": "active"
}

Response: { "id": 1, "name": "...", ... }


# Get all projects
GET /api/v1/projects
Authorization: Bearer {access_token}

Response: [ { "id": 1, "name": "...", ... } ]


# Get specific project
GET /api/v1/projects/{id}
Authorization: Bearer {access_token}

Response: { "id": 1, "name": "...", ... }


# Update project
PUT /api/v1/projects/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Updated name",
  "status": "completed"
}

Response: { "id": 1, "name": "Updated name", ... }


# Delete project
DELETE /api/v1/projects/{id}
Authorization: Bearer {access_token}

Response: 204 No Content


# Create research session
POST /api/v1/projects/{id}/sessions
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "session_name": "Phase 1 Analysis"
}

Response: { "id": 1, "project_id": 1, "name": "Phase 1 Analysis", ... }
```

### Agents (`/api/v1/agents`)

```bash
# Execute agent
POST /api/v1/agents/{agent_type}/execute
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "session_id": 1,
  "input": {
    "molecule": "Aspirin",
    "target": "inflammation",
    "parameters": { ... }
  }
}

Response: { "id": 1, "session_id": 1, "status": "pending", ... }


# Valid agent types:
# - research
# - market_intelligence
# - formulation
# - safety
# - regulatory
# - competitive_intelligence
# - medical_writing
# - patent_ip


# Get agent request history
GET /api/v1/agents/history?limit=50&offset=0
Authorization: Bearer {access_token}

Response: {
  "total": 5,
  "requests": [ { "id": 1, ... }, ... ]
}


# Get specific agent request
GET /api/v1/agents/{request_id}
Authorization: Bearer {access_token}

Response: { "id": 1, "session_id": 1, ... }
```

### Documents (`/api/v1/documents`)

```bash
# Upload document
POST /api/v1/documents/upload?project_id=1
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

file: <binary_file>

Response: {
  "id": 1,
  "message": "File uploaded successfully",
  "file_name": "research.pdf",
  "file_size": 2048576
}


# Get document details
GET /api/v1/documents/{id}
Authorization: Bearer {access_token}

Response: {
  "id": 1,
  "project_id": 1,
  "file_name": "research.pdf",
  "file_type": "pdf",
  ...
}


# Delete document
DELETE /api/v1/documents/{id}
Authorization: Bearer {access_token}

Response: 204 No Content
```

## Environment Configuration

The `.env` file contains all configuration:

```env
# App
APP_NAME=PharmaPilot
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/pharmapilot
DATABASE_SYNC_URL=postgresql://postgres:password@localhost:5432/pharmapilot

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=pharma-pilot-secret-key-change-in-production-32-chars-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS (for frontend)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# File upload
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads
```

### Production Settings

Change these for production:
1. **DEBUG**: Set to `False`
2. **ENVIRONMENT**: Set to `production`
3. **SECRET_KEY**: Use a strong, random 32+ character key
4. **DATABASE_URL**: Use production PostgreSQL instance
5. **REDIS_URL**: Use production Redis instance
6. **CORS_ORIGINS**: Add your frontend domain

## Testing

### Manual Testing with cURL

```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "full_name": "Test User",
    "role": "researcher"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Create project (replace TOKEN with actual access_token)
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "molecule_name": "TestMol",
    "indication": "Testing"
  }'
```

### Using FastAPI Interactive Docs

1. Go to http://localhost:8000/docs
2. Click "Authorize" button (top right)
3. Login to get token
4. Click "Try it out" on any endpoint
5. Fill in parameters and click "Execute"

## Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique email address
- `hashed_password` - Bcrypt hashed password
- `full_name` - User's full name
- `role` - User role (researcher, admin, etc.)
- `is_active` - Account active status
- `created_at`, `updated_at` - Timestamps

### Projects Table
- `id` - Primary key
- `name`, `description` - Project info
- `molecule_name`, `indication` - Research details
- `status` - Project status (active, completed, etc.)
- `owner_id` - FK to Users
- `created_at`, `updated_at` - Timestamps

### ResearchSessions Table
- `id` - Primary key
- `project_id` - FK to Projects
- `name` - Session name
- `created_at` - Timestamp

### AgentRequests Table
- `id` - Primary key
- `session_id` - FK to ResearchSessions
- `user_id` - FK to Users
- `agent_type` - Agent type enum
- `input_data`, `output_data` - JSON data
- `status` - Request status (pending, completed, error)
- `tokens_used` - Token count for AI usage
- `created_at` - Timestamp

### Documents Table
- `id` - Primary key
- `project_id` - FK to Projects
- `file_name`, `file_path`, `file_type`, `file_size` - File info
- `uploaded_by` - FK to Users
- `created_at` - Timestamp

## Integration with Frontend

### Setup Frontend Connection

```javascript
// Frontend configuration (React/Vue/Angular)
const API_BASE_URL = "http://localhost:8000";

// Example: Login
async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("refresh_token", data.refresh_token);
}

// Example: Protected request
async function getProjects() {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${API_BASE_URL}/api/v1/projects`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });
  
  return response.json();
}
```

## Common Issues & Solutions

### PostgreSQL Connection Error
```
sqlalchemy.exc.OperationalError: could not translate host name
```
**Solution**: Ensure PostgreSQL container is running
```bash
docker-compose up -d
docker-compose logs postgres
```

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change port in `.env` or kill process on port 8000

### Module Not Found
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Database Tables Not Created
**Solution**: Restart the server - tables auto-create on startup

## Stopping Services

```bash
# Stop FastAPI server
# Press Ctrl+C in terminal

# Stop Docker containers
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Production Deployment

### With Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### With Docker

```bash
# Build image
docker build -t pharmapilot-backend .

# Run container
docker run -p 8000:8000 --env-file .env pharmapilot-backend
```

## Agent Integration

The backend provides an interface for AI agents to integrate:

1. **Agent executes request**:
   ```
   POST /api/v1/agents/{agent_type}/execute
   ```

2. **Backend stores request** in database with status "pending"

3. **Agent polls or receives webhook** for request details

4. **Agent processes** and calls update endpoint

5. **Backend updates request** with results and status "completed"

Example agent flow:
```python
# Agent code (running separately)
import requests

response = requests.post(
    "http://localhost:8000/api/v1/agents/research/execute",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "session_id": 1,
        "input": {"molecule": "Aspirin", "target": "inflammation"}
    }
)

request_id = response.json()["id"]

# Process research...
results = process_research_query(...)

# Update backend with results
requests.put(
    f"http://localhost:8000/api/v1/agents/{request_id}",
    headers={"Authorization": f"Bearer {token}"},
    json={"status": "completed", "output": results}
)
```

## Logging & Debugging

### Enable Detailed Logging

```python
# In app/main.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### View Database Logs

```bash
# See SQL queries
docker-compose logs postgres

# View all logs
docker-compose logs
```

## Performance Tips

1. **Use connection pooling** (already configured)
2. **Enable Redis caching** for repeated queries
3. **Index frequently queried fields** (already done for foreign keys)
4. **Use pagination** for large datasets
5. **Monitor with uvicorn logs**

## Security Checklist

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens with expiration
- ✅ CORS validation
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ File upload size limits
- ✅ Role-based access control

**Additional for production:**
- Use HTTPS/SSL
- Implement rate limiting
- Add input sanitization
- Use environment-specific secrets
- Enable CSRF protection
- Add request logging/monitoring

## Support & Documentation

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **PostgreSQL Docs**: https://www.postgresql.org/docs
- **Redis Docs**: https://redis.io/documentation

## License

© 2024 PharmaPilot. All rights reserved.
