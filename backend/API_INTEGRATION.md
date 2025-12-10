# PharmaPilot API Integration Guide

## Overview

PharmaPilot's backend is built with FastAPI and provides a RESTful API for pharmaceutical research management. The system consists of three main modules: Authentication, Project Management, and AI Agent Integration.

## Architecture

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    Client    │◄───────►│   Backend    │◄───────►│  PostgreSQL  │
│  (React UI)  │   HTTP  │   (FastAPI)  │   ORM   │   Database   │
└──────────────┘         └──────────────┘         └──────────────┘
                                │
                                │
                         ┌──────▼──────┐
                         │  AI Agents  │
                         │  (External) │
                         └─────────────┘
```

## Base URL

- Development: `http://localhost:8000`
- API Version: `v1`
- API Prefix: `/api/v1`

## Authentication Flow

### JWT Token-Based Authentication

The system uses JSON Web Tokens (JWT) for secure authentication with two token types:

1. **Access Token**: Short-lived (30 minutes) - used for API requests
2. **Refresh Token**: Long-lived (7 days) - used to obtain new access tokens

### Token Storage (Client-Side)

The client stores tokens in localStorage after successful authentication:

```javascript
// authApi.js implementation
localStorage.setItem('accessToken', response.access_token);
localStorage.setItem('refreshToken', response.refresh_token);
```

### Request Authentication

All protected endpoints require the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## API Endpoints

### 1. Authentication Endpoints

#### POST `/api/v1/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "researcher@pharma.com",
  "full_name": "Dr. Jane Smith",
  "password": "SecurePass123",
  "role": "researcher"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "researcher@pharma.com",
  "full_name": "Dr. Jane Smith",
  "role": "researcher",
  "is_active": true,
  "created_at": "2025-12-09T10:30:00",
  "updated_at": "2025-12-09T10:30:00"
}
```

**Client Integration:**
```javascript
// authApi.js - register function
const response = await fetch(`${API_BASE_URL}/auth/register`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(userData)
});
```

**Validation:**
- Email must be valid and unique
- Password must be at least 8 characters
- All fields are required

---

#### POST `/api/v1/auth/login`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "researcher@pharma.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Client Integration:**
```javascript
// authApi.js - login function
const response = await fetch(`${API_BASE_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});

const data = await response.json();
localStorage.setItem('accessToken', data.access_token);
localStorage.setItem('refreshToken', data.refresh_token);
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `400 Bad Request`: Missing fields

---

#### GET `/api/v1/auth/me`

Get current authenticated user information.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "researcher@pharma.com",
  "full_name": "Dr. Jane Smith",
  "role": "researcher",
  "is_active": true,
  "created_at": "2025-12-09T10:30:00",
  "updated_at": "2025-12-09T10:30:00"
}
```

**Client Integration:**
```javascript
const response = await fetch(`${API_BASE_URL}/auth/me`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});
```

---

#### POST `/api/v1/auth/refresh`

Refresh an expired access token using a refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Client Integration:**
```javascript
// Automatic token refresh on 401 errors
if (response.status === 401) {
  const refreshToken = localStorage.getItem('refreshToken');
  const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  
  const newTokens = await refreshResponse.json();
  localStorage.setItem('accessToken', newTokens.access_token);
  localStorage.setItem('refreshToken', newTokens.refresh_token);
}
```

---

#### POST `/api/v1/auth/forgot-password`

Request a password reset link (mock implementation for security).

**Request Body:**
```json
{
  "email": "researcher@pharma.com"
}
```

**Response (200 OK):**
```json
{
  "detail": "If this email is registered, a password reset link has been sent."
}
```

---

### 2. Project Management Endpoints

#### GET `/api/v1/projects`

Retrieve all projects for the authenticated user.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "Aspirin Research Project",
    "molecule_name": "Acetylsalicylic Acid",
    "description": "Investigating new formulations of aspirin",
    "status": "active",
    "created_at": "2025-12-01T08:00:00",
    "updated_at": "2025-12-09T10:30:00"
  },
  {
    "id": 2,
    "user_id": 1,
    "name": "Ibuprofen Study",
    "molecule_name": "Ibuprofen",
    "description": "Patent landscape analysis",
    "status": "active",
    "created_at": "2025-12-05T14:20:00",
    "updated_at": "2025-12-05T14:20:00"
  }
]
```

**Client Integration:**
```javascript
const response = await fetch(`${API_BASE_URL}/projects`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});
const projects = await response.json();
```

---

#### POST `/api/v1/projects`

Create a new research project.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "New Drug Research",
  "molecule_name": "Compound-X",
  "description": "Exploring patent opportunities for Compound-X"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "user_id": 1,
  "name": "New Drug Research",
  "molecule_name": "Compound-X",
  "description": "Exploring patent opportunities for Compound-X",
  "status": "active",
  "created_at": "2025-12-09T11:00:00",
  "updated_at": "2025-12-09T11:00:00"
}
```

**Client Integration:**
```javascript
const response = await fetch(`${API_BASE_URL}/projects`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
  body: JSON.stringify(projectData)
});
```

---

#### GET `/api/v1/projects/{project_id}`

Get details of a specific project.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**URL Parameters:**
- `project_id` (integer): The project ID

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Aspirin Research Project",
  "molecule_name": "Acetylsalicylic Acid",
  "description": "Investigating new formulations of aspirin",
  "status": "active",
  "created_at": "2025-12-01T08:00:00",
  "updated_at": "2025-12-09T10:30:00"
}
```

**Error Responses:**
- `404 Not Found`: Project doesn't exist or doesn't belong to user

---

#### PUT `/api/v1/projects/{project_id}`

Update an existing project.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**URL Parameters:**
- `project_id` (integer): The project ID

**Request Body (all fields optional):**
```json
{
  "name": "Updated Project Name",
  "molecule_name": "Updated Molecule",
  "description": "Updated description",
  "status": "completed"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Updated Project Name",
  "molecule_name": "Updated Molecule",
  "description": "Updated description",
  "status": "completed",
  "created_at": "2025-12-01T08:00:00",
  "updated_at": "2025-12-09T11:15:00"
}
```

**Client Integration:**
```javascript
const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
  body: JSON.stringify(updates)
});
```

---

#### DELETE `/api/v1/projects/{project_id}`

Delete a project and all associated data.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**URL Parameters:**
- `project_id` (integer): The project ID

**Response (204 No Content):**
- Empty response body on success

**Client Integration:**
```javascript
await fetch(`${API_BASE_URL}/projects/${projectId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});
```

---

### 3. AI Agent Integration Endpoints

#### POST `/api/v1/agents/execute`

Execute an AI agent and log the results.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "project_id": 1,
  "agent_type": "patent_search",
  "input_text": "Search for aspirin-related patents filed after 2020"
}
```

**Agent Types:**
- `patent_search`: USPTO patent database search
- `market_analysis`: Market opportunity analysis
- `competitor_analysis`: Competitive landscape research
- `clinical_trials`: Clinical trial data retrieval
- `regulatory_analysis`: Regulatory pathway analysis

**Response (200 OK):**
```json
{
  "id": 1,
  "project_id": 1,
  "agent_type": "patent_search",
  "input_text": "Search for aspirin-related patents filed after 2020",
  "output_text": "Agent execution result will appear here",
  "status": "completed",
  "created_at": "2025-12-09T11:30:00"
}
```

**Client Integration:**
```javascript
// responseGenerator.js integration
const response = await fetch(`${API_BASE_URL}/agents/execute`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  },
  body: JSON.stringify({
    project_id: currentProjectId,
    agent_type: 'patent_search',
    input_text: userQuery
  })
});
```

**AI Agent Developer Integration:**

External AI agents should call this endpoint to log their execution:

```python
# AI Agent (Python example)
import requests

def log_agent_execution(project_id, agent_type, input_text, output_text, access_token):
    response = requests.post(
        "http://localhost:8000/api/v1/agents/execute",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={
            "project_id": project_id,
            "agent_type": agent_type,
            "input_text": input_text
        }
    )
    return response.json()
```

---

#### GET `/api/v1/agents/logs`

Retrieve execution logs for AI agents.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**Query Parameters (optional):**
- `project_id` (integer): Filter logs by project

**Response (200 OK):**
```json
[
  {
    "id": 5,
    "project_id": 1,
    "agent_type": "patent_search",
    "input_text": "Find patents for aspirin formulations",
    "output_text": "Found 47 patents matching criteria...",
    "status": "completed",
    "created_at": "2025-12-09T11:30:00"
  },
  {
    "id": 4,
    "project_id": 1,
    "agent_type": "market_analysis",
    "input_text": "Analyze aspirin market opportunity",
    "output_text": "Market size: $2.3B, Growth: 4.5%...",
    "status": "completed",
    "created_at": "2025-12-09T10:15:00"
  }
]
```

**Client Integration:**
```javascript
// Get all logs
const response = await fetch(`${API_BASE_URL}/agents/logs`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

// Get logs for specific project
const projectLogs = await fetch(`${API_BASE_URL}/agents/logs?project_id=1`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});
```

---

#### GET `/api/v1/agents/logs/{log_id}`

Get details of a specific agent execution log.

**Headers Required:**
```
Authorization: Bearer <access_token>
```

**URL Parameters:**
- `log_id` (integer): The log entry ID

**Response (200 OK):**
```json
{
  "id": 5,
  "project_id": 1,
  "agent_type": "patent_search",
  "input_text": "Find patents for aspirin formulations",
  "output_text": "Found 47 patents matching criteria. Top results include...",
  "status": "completed",
  "created_at": "2025-12-09T11:30:00"
}
```

**Error Responses:**
- `404 Not Found`: Log doesn't exist or doesn't belong to user's projects

---

## Client-Backend Integration Details

### AppContext State Management

The `AppContext.jsx` manages global application state including:

```javascript
const AppContext = createContext({
  user: null,              // Current user object
  isAuthenticated: false,  // Authentication status
  currentProject: null,    // Active project
  projects: [],           // All user projects
  agentLogs: []          // Agent execution logs
});
```

### Authentication Flow in Client

```javascript
// Login flow (Login.jsx)
1. User submits credentials
2. authApi.login() calls POST /api/v1/auth/login
3. Store access_token and refresh_token in localStorage
4. Update AppContext with user data
5. Redirect to dashboard

// Protected Route Access
1. Component checks AppContext.isAuthenticated
2. If false, redirect to login
3. If true, include Authorization header in requests
4. Handle 401 by refreshing token
```

### API Request Pattern

```javascript
// Standard authenticated request
async function makeAuthenticatedRequest(endpoint, options = {}) {
  const accessToken = localStorage.getItem('accessToken');
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      ...options.headers
    }
  });
  
  if (response.status === 401) {
    // Token expired, refresh it
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      // Retry request with new token
      return makeAuthenticatedRequest(endpoint, options);
    } else {
      // Refresh failed, logout user
      logout();
    }
  }
  
  return response;
}
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,  -- bcrypt hashed
    role VARCHAR(50) DEFAULT 'researcher',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    molecule_name VARCHAR(255),
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Agent Logs Table
```sql
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    agent_type VARCHAR(100) NOT NULL,
    input_text TEXT,
    output_text TEXT,
    status VARCHAR(50) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Security Considerations

### Password Security
- Passwords hashed using bcrypt with automatic salt generation
- Minimum password length: 8 characters
- Never returned in API responses

### Token Security
- JWT tokens signed with HS256 algorithm
- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Token type validation prevents token misuse

### Authorization
- All project and agent endpoints verify ownership
- Users can only access their own data
- Cascade deletes prevent orphaned records

### CORS Configuration
```python
# Allowed origins for client connections
CORS_ORIGINS = "http://localhost:3000,http://localhost:5173"
```

---

## Error Handling

### Standard Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server-side error |

---

## Environment Configuration

### Backend (.env file)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/pharmapilot
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Client (authApi.js)
```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

---

## Development Workflow

### Starting the Backend
```powershell
cd backend
.\start.ps1

# Or manually:
docker-compose up -d
uvicorn app.main:app --reload --port 8000
```

### Starting the Client
```powershell
cd Client
npm install
npm run dev
```

### API Documentation
Once the backend is running, access interactive documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## AI Agent Development Guide

### Creating a New AI Agent

1. **Choose an Agent Type**: Decide on functionality (e.g., patent_search, market_analysis)

2. **Implement Agent Logic**: Create your AI processing logic

3. **Integrate with Backend API**:
```python
import requests

class PatentSearchAgent:
    def __init__(self, api_base_url, access_token):
        self.api_base_url = api_base_url
        self.access_token = access_token
    
    def execute(self, project_id, query):
        # Your AI agent logic here
        result = self.search_patents(query)
        
        # Log execution to backend
        response = requests.post(
            f"{self.api_base_url}/agents/execute",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            },
            json={
                "project_id": project_id,
                "agent_type": "patent_search",
                "input_text": query
            }
        )
        
        return response.json()
```

4. **Test Integration**: Use the `/agents/logs` endpoint to verify logging

---

## Deployment Checklist

### Security
- [ ] Change SECRET_KEY in production
- [ ] Use strong database passwords
- [ ] Enable HTTPS
- [ ] Restrict CORS origins
- [ ] Set up rate limiting
- [ ] Enable database backups

### Environment
- [ ] Set production DATABASE_URL
- [ ] Configure production CORS_ORIGINS
- [ ] Set appropriate token expiration times
- [ ] Use environment variables for secrets

### Monitoring
- [ ] Set up error logging
- [ ] Monitor API response times
- [ ] Track authentication failures
- [ ] Monitor database connections

---

## Support and Maintenance

### Health Check
```bash
curl http://localhost:8000/health
```

### Database Migrations
```bash
# If using Alembic for migrations
alembic upgrade head
```

### Logs
```bash
# View application logs
docker-compose logs -f backend

# View database logs
docker-compose logs -f postgres
```

---

## Conclusion

This API provides a complete backend solution for pharmaceutical research management, with secure authentication, project management, and AI agent integration. The architecture supports scalable development and easy integration with external AI services.

For questions or issues, refer to the interactive API documentation at `/docs` when the server is running.
