# PharmaPilot Backend

Enterprise-grade RESTful API for pharmaceutical research management, built with FastAPI and PostgreSQL.

## Features

- **Secure Authentication**: JWT-based authentication with access and refresh tokens
- **Project Management**: Complete CRUD operations for research projects
- **AI Agent Integration**: Standardized interface for AI-powered research tools
- **Database Persistence**: PostgreSQL with SQLAlchemy ORM
- **Interactive Documentation**: Auto-generated Swagger/OpenAPI docs
- **Docker Support**: Containerized deployment ready

## Technology Stack

- **Framework**: FastAPI 0.100+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose), bcrypt
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker & Docker Compose

## Project Structure

```
Server/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── auth.py              # Authentication logic
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── projects.py      # Project management endpoints
│       └── agents.py        # AI agent integration endpoints
├── docker-compose.yml       # Container orchestration
├── requirements.txt         # Python dependencies
├── API_INTEGRATION.md       # Comprehensive API documentation
├── ARCHITECTURE.md          # System architecture details
└── README_BACKEND.md        # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 15+ (or Docker)
- pip

### Installation

1. **Clone the repository**
```powershell
cd backend
```

2. **Create virtual environment** (optional but recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Start PostgreSQL**

Using Docker:
```powershell
docker-compose up -d postgres
```

Or use your local PostgreSQL instance and update `DATABASE_URL` in `.env`

5. **Configure environment**

Create a `.env` file:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/pharmapilot
SECRET_KEY=your-production-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

6. **Run the application**

```powershell
uvicorn app.main:app --reload --port 8000
```

Or use the provided script:
```powershell
.\start.ps1
```

### Verification

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to access the interactive API documentation.

Test the health endpoint:
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and receive tokens |
| GET | `/api/v1/auth/me` | Get current user info |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/forgot-password` | Request password reset |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects` | List all user projects |
| POST | `/api/v1/projects` | Create new project |
| GET | `/api/v1/projects/{id}` | Get project details |
| PUT | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Delete project |

### AI Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/agents/execute` | Execute AI agent |
| GET | `/api/v1/agents/logs` | Get agent execution logs |
| GET | `/api/v1/agents/logs/{id}` | Get specific log entry |

For detailed API documentation with request/response examples, see [API_INTEGRATION.md](./API_INTEGRATION.md).

## Database Schema

### Users
- id, email, full_name, password (hashed), role, is_active, timestamps

### Projects
- id, user_id, name, molecule_name, description, status, timestamps

### Agent Logs
- id, project_id, agent_type, input_text, output_text, status, created_at

Relationships:
- Users → Projects (one-to-many)
- Projects → Agent Logs (one-to-many)
- Cascade deletes maintain referential integrity

## Security

### Authentication
- Passwords hashed with bcrypt (automatic salt generation)
- JWT tokens with HS256 algorithm
- Access tokens: 30 minutes validity
- Refresh tokens: 7 days validity
- Token type validation prevents misuse

### Authorization
- All endpoints verify user ownership of resources
- Users can only access their own data
- Database constraints prevent data inconsistency

### Best Practices
- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting
- Regular security audits

## Development

### Running Tests

```powershell
pytest
```

### Code Formatting

```powershell
black app/
```

### Linting

```powershell
flake8 app/
```

### Database Migrations

If using Alembic:
```powershell
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Docker Deployment

### Full Stack

```powershell
docker-compose up -d
```

This starts:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)

### Database Only

```powershell
docker-compose up -d postgres
```

### View Logs

```powershell
docker-compose logs -f backend
```

### Stop Services

```powershell
docker-compose down
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:password@localhost:5432/pharmapilot |
| SECRET_KEY | JWT signing key | (must be changed in production) |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token lifetime | 30 |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token lifetime | 7 |
| API_V1_PREFIX | API version prefix | /api/v1 |
| CORS_ORIGINS | Allowed CORS origins | http://localhost:3000,http://localhost:5173 |

### CORS Configuration

Update `CORS_ORIGINS` in `.env` to allow your frontend domain:

```env
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
```

## Troubleshooting

### Database Connection Failed

**Problem**: Cannot connect to PostgreSQL

**Solutions**:
1. Ensure PostgreSQL is running: `docker-compose ps`
2. Check DATABASE_URL in `.env`
3. Verify PostgreSQL credentials
4. Check port availability: `netstat -an | findstr 5432`

### Authentication Errors

**Problem**: 401 Unauthorized responses

**Solutions**:
1. Verify token is included in Authorization header
2. Check token hasn't expired
3. Ensure SECRET_KEY matches between token generation and validation
4. Try refreshing the token

### CORS Errors

**Problem**: Browser blocks requests from frontend

**Solutions**:
1. Add frontend URL to `CORS_ORIGINS` in `.env`
2. Restart backend after configuration changes
3. Verify frontend is using correct API URL

### Import Errors

**Problem**: Module not found errors

**Solutions**:
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version is 3.9+
3. Verify virtual environment is activated

## Performance Optimization

### Database Connection Pooling

SQLAlchemy automatically manages connection pooling. For production:

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=40
)
```

### Caching

Consider implementing Redis for:
- Session management
- Frequently accessed data
- Rate limiting

### Load Balancing

Use Nginx or similar for:
- Multiple Uvicorn workers
- SSL termination
- Static file serving

## Monitoring and Logging

### Application Logs

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Health Checks

```bash
curl http://localhost:8000/health
```

### Database Monitoring

```sql
SELECT * FROM pg_stat_activity;
```

## Production Deployment

### Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Use production-grade PostgreSQL instance
- [ ] Enable HTTPS/SSL
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and alerting
- [ ] Enable database backups
- [ ] Implement rate limiting
- [ ] Set up log aggregation
- [ ] Configure firewall rules
- [ ] Use environment-specific configuration
- [ ] Set up CI/CD pipeline
- [ ] Enable auto-scaling (if cloud deployed)

### Recommended Services

- **Hosting**: AWS (ECS/Fargate), Google Cloud Run, Azure Container Apps
- **Database**: AWS RDS, Google Cloud SQL, Azure Database
- **Monitoring**: DataDog, New Relic, Prometheus + Grafana
- **Logging**: ELK Stack, Splunk, CloudWatch

## AI Agent Integration

To integrate external AI agents:

1. **Authenticate**: Obtain access token via `/auth/login`
2. **Execute**: POST to `/agents/execute` with:
   - `project_id`: Target project
   - `agent_type`: Your agent identifier
   - `input_text`: Query or parameters
3. **Retrieve Results**: GET `/agents/logs` to fetch execution history

Example Python integration:

```python
import requests

class MyAgent:
    def __init__(self, api_url, access_token):
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    def execute(self, project_id, query):
        response = requests.post(
            f"{self.api_url}/agents/execute",
            headers=self.headers,
            json={
                "project_id": project_id,
                "agent_type": "my_custom_agent",
                "input_text": query
            }
        )
        return response.json()
```

## Support

For detailed integration guide, see [API_INTEGRATION.md](./API_INTEGRATION.md).

For architecture details, see [ARCHITECTURE.md](./ARCHITECTURE.md).

For issues or questions, refer to the interactive documentation at `/docs` when running the server.

## License

This project is proprietary software. All rights reserved.

## Contributors

Developed for pharmaceutical research automation and AI agent integration.
