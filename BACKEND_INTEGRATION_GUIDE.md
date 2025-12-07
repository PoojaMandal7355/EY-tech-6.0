# PharmaPilot Backend Integration Guide

This document provides comprehensive specifications for implementing backend logic to integrate with the PharmaPilot frontend. Use this as a reference for implementing all required API endpoints and business logic.

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Chat & AI Response Generation](#chat--ai-response-generation)
4. [PDF Document Management](#pdf-document-management)
5. [Response Features](#response-features)
6. [Report Generation & Download](#report-generation--download)
7. [Database Schema](#database-schema)
8. [API Endpoints Summary](#api-endpoints-summary)

---

## Overview

PharmaPilot is a pharmaceutical research assistant platform with the following core features:

- **User Authentication**: JWT-based user registration and login
- **Chat Interface**: Real-time AI responses with typing animation
- **PDF Upload**: Process pharmaceutical documents for analysis
- **Markdown Rendering**: Display formatted responses with code blocks
- **Data Visualization**: Charts and graphs in responses
- **Report Generation**: Export chat history and analysis as PDF
- **Message Regeneration**: Re-generate AI responses with improved prompts

### Technology Stack

**Frontend**:
- React 19 with Hooks & Context API
- Vite (build tool)
- Tailwind CSS
- Chart.js for data visualization
- jsPDF + html2canvas for PDF export
- React Markdown for rendering

**Backend** (Expected):
- FastAPI (Python)
- PostgreSQL Database
- SQLAlchemy ORM
- JWT Authentication
- PDF processing library (PyPDF2 or pdfplumber)

---

## Authentication

Authentication is already implemented in the backend. Ensure these endpoints work correctly:

### Existing Auth Endpoints

#### POST `/api/v1/auth/register`
Register a new user.

**Request**:
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "researcher",
  "is_active": true,
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T10:30:00Z"
}
```

#### POST `/api/v1/auth/login`
Login with email and password.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET `/api/v1/auth/me`
Get current authenticated user.

**Headers**: `Authorization: Bearer {access_token}`

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "researcher",
  "is_active": true,
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T10:30:00Z"
}
```

#### POST `/api/v1/auth/refresh`
Refresh access token.

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### POST `/api/v1/auth/forgot-password`
Request a password reset link to be emailed to the user.

**Request**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200 OK):
```json
{
  "detail": "If this email is registered, a reset link has been sent"
}
```

#### POST `/api/v1/auth/reset-password`
Apply password reset using a token from the email link.

**Request**:
```json
{
  "token": "reset-token-from-email",
  "new_password": "NewSecurePassword123"
}
```

**Response** (200 OK):
```json
{
  "detail": "Password updated successfully"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Chat & AI Response Generation

### NEW ENDPOINT: POST `/api/v1/chat/generate`

Generate AI response for user prompt. This is the **most important endpoint** for the chat functionality.

#### Request

**Headers**: `Authorization: Bearer {access_token}`

**Body**:
```json
{
  "prompt": "What are the common side effects of aspirin?",
  "session_id": 1,
  "upload_file_id": null
}
```

**Parameters**:
- `prompt` (string, required): User's question or input
- `session_id` (integer, required): Chat session ID (can start with 1)
- `upload_file_id` (integer, optional): ID of uploaded PDF if analyzing a document

#### Response (200 OK)

```json
{
  "id": 1,
  "content": "Aspirin, also known as acetylsalicylic acid...\n\n## Common Side Effects:\n1. Gastrointestinal issues\n2. Bleeding risk\n...",
  "charts": [
    {
      "type": "bar",
      "title": "Side Effect Frequency",
      "labels": ["GI Issues", "Bleeding", "Allergic"],
      "datasets": [
        {
          "label": "Occurrence %",
          "data": [45, 30, 10],
          "backgroundColor": ["#10b981", "#3b82f6", "#f59e0b"]
        }
      ]
    }
  ],
  "timestamp": "2025-12-07T10:35:00Z",
  "tokens_used": 450
}
```

#### Response Content Structure

The `content` field should be **Markdown formatted** with:
- Headers (# ## ###)
- Bold text (**text**)
- Lists (- or 1.)
- Code blocks (```python or ```json)
- Links [text](url)
- Tables (if needed)

#### Charts Structure

Charts are **Chart.js compatible** objects. Each chart must have:

```json
{
  "type": "bar|line|pie|doughnut",
  "title": "Chart Title",
  "labels": ["Label 1", "Label 2"],
  "datasets": [
    {
      "label": "Dataset Name",
      "data": [10, 20, 30],
      "backgroundColor": ["#10b981", "#3b82f6", "#f59e0b"],
      "borderColor": "#ffffff",
      "borderWidth": 1
    }
  ]
}
```

**Supported Chart Types**:
- `bar` - Bar chart
- `line` - Line chart
- `pie` - Pie chart
- `doughnut` - Doughnut chart
- `radar` - Radar chart
- `bubble` - Bubble chart

#### Implementation Notes

1. **AI Integration**: Use OpenAI API, Claude API, or another LLM service
2. **Response Formatting**: Ensure markdown formatting for rich text display
3. **Chart Generation**: Dynamically generate charts based on data analysis
4. **Streaming** (Optional): Consider implementing streaming for real-time typing animation
5. **Token Tracking**: Count and return tokens used for rate limiting/billing
6. **Error Handling**: Return meaningful error messages

#### Example Implementation Flow

```python
@router.post("/api/v1/chat/generate", response_model=ChatResponse)
async def generate_response(
    request: ChatGenerateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    # 1. Validate session belongs to user
    # 2. Get uploaded document if file_id provided
    # 3. Build context from document + history
    # 4. Call LLM with prompt
    # 5. Parse response for markdown + data
    # 6. Generate charts if data detected
    # 7. Save message to database
    # 8. Return formatted response
```

---

## PDF Document Management

### NEW ENDPOINT: POST `/api/v1/documents/upload`

Upload and process a PDF document for pharmaceutical analysis.

#### Request

**Headers**: 
- `Authorization: Bearer {access_token}`
- `Content-Type: multipart/form-data`

**Body**:
```
POST /api/v1/documents/upload
Content-Disposition: form-data; name="file"; filename="research.pdf"
[PDF file binary data]
```

#### Response (201 Created)

```json
{
  "id": 1,
  "user_id": 1,
  "filename": "research.pdf",
  "original_filename": "research.pdf",
  "file_size": 2048576,
  "upload_timestamp": "2025-12-07T10:30:00Z",
  "status": "processed",
  "extracted_text_preview": "This research paper discusses...[first 200 chars]",
  "page_count": 15,
  "content_summary": "Research on drug efficacy and side effects"
}
```

#### Implementation Notes

1. **File Validation**:
   - Only allow .pdf files
   - Maximum file size: 50MB
   - Validate PDF structure

2. **PDF Processing**:
   - Extract text using PyPDF2 or pdfplumber
   - Extract tables if present
   - Store extracted text in database
   - Generate preview/summary

3. **Storage**:
   - Save original file to filesystem or cloud storage
   - Store extracted text in database
   - Index content for search

4. **Response Data**:
   - Include text preview for frontend display
   - Calculate and return page count
   - Generate content summary (first 100 words)

### NEW ENDPOINT: GET `/api/v1/documents/{document_id}`

Retrieve uploaded document details and extracted content.

#### Request

**Headers**: `Authorization: Bearer {access_token}`

**URL Parameters**:
- `document_id` (integer): ID of document to retrieve

#### Response (200 OK)

```json
{
  "id": 1,
  "user_id": 1,
  "filename": "research.pdf",
  "original_filename": "research.pdf",
  "file_size": 2048576,
  "upload_timestamp": "2025-12-07T10:30:00Z",
  "status": "processed",
  "page_count": 15,
  "extracted_text": "Full extracted text from PDF...",
  "tables": [
    {
      "page": 5,
      "table_number": 1,
      "content": "[[row1col1, row1col2], [row2col1, row2col2]]"
    }
  ],
  "content_summary": "Research on drug efficacy"
}
```

---

## Response Features

### Message History & Regeneration

#### NEW ENDPOINT: POST `/api/v1/messages`

Save chat message (user or assistant).

#### Request

```json
{
  "session_id": 1,
  "role": "user|assistant",
  "content": "What are the side effects?",
  "message_type": "text|analysis",
  "related_document_id": null
}
```

#### Response (201 Created)

```json
{
  "id": 1,
  "session_id": 1,
  "user_id": 1,
  "role": "user",
  "content": "What are the side effects?",
  "message_type": "text",
  "related_document_id": null,
  "timestamp": "2025-12-07T10:35:00Z"
}
```

#### NEW ENDPOINT: POST `/api/v1/messages/{message_id}/regenerate`

Regenerate AI response for a specific message.

**Request**:
```json
{
  "improved_prompt": "Provide a more detailed analysis of side effects with percentages"
}
```

**Response**:
```json
{
  "id": 2,
  "session_id": 1,
  "role": "assistant",
  "content": "Updated response with more details...",
  "charts": [...],
  "timestamp": "2025-12-07T10:36:00Z",
  "is_regenerated": true,
  "original_message_id": 1
}
```

#### NEW ENDPOINT: GET `/api/v1/sessions/{session_id}/messages`

Get chat history for a session.

**Request**:
```
GET /api/v1/sessions/1/messages?limit=50&offset=0
```

**Response** (200 OK):
```json
{
  "total": 12,
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "What are the side effects?",
      "timestamp": "2025-12-07T10:35:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Aspirin side effects...",
      "charts": [...],
      "timestamp": "2025-12-07T10:35:30Z"
    }
  ]
}
```

---

## Report Generation & Download

### NEW ENDPOINT: POST `/api/v1/reports/generate`

Generate a PDF report from chat session.

#### Request

```json
{
  "session_id": 1,
  "title": "Aspirin Research Analysis",
  "include_metadata": true,
  "include_charts": true,
  "include_original_documents": true
}
```

#### Response (200 OK)

```json
{
  "id": 1,
  "session_id": 1,
  "filename": "report_session_1_2025_12_07.pdf",
  "file_size": 4096000,
  "generated_at": "2025-12-07T10:40:00Z",
  "download_url": "/api/v1/reports/1/download"
}
```

#### Report Content Structure

The generated PDF should include:

1. **Cover Page**:
   - Title
   - User name
   - Generation date
   - Company/Platform logo

2. **Table of Contents**:
   - Auto-generated from sections

3. **Executive Summary**:
   - Overview of analysis
   - Key findings

4. **Chat History**:
   - All user questions
   - AI responses (formatted from markdown)
   - Charts/graphs embedded
   - Timestamps

5. **Uploaded Documents Summary** (if applicable):
   - Document names
   - Upload dates
   - Key extracts

6. **Conclusion**:
   - Summary of findings
   - Recommendations

#### Implementation Notes

1. **PDF Generation**:
   - Use reportlab or weasyprint for PDF generation
   - Ensure charts are rendered as images
   - Format markdown to proper PDF styles

2. **File Storage**:
   - Save generated PDF to filesystem
   - Store metadata in database
   - Keep for 30 days then auto-delete

3. **Error Handling**:
   - Handle large chat histories
   - Gracefully handle charts that won't render
   - Provide meaningful error messages

### NEW ENDPOINT: GET `/api/v1/reports/{report_id}/download`

Download generated PDF report.

#### Request

**Headers**: `Authorization: Bearer {access_token}`

#### Response (200 OK)

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="report_session_1_2025_12_07.pdf"
[PDF file binary data]
```

#### Implementation Notes

1. **Security**:
   - Verify user owns the report
   - Check authorization
   - Log download for audit

2. **Performance**:
   - Cache generated PDFs
   - Stream large files
   - Implement compression if needed

---

## Database Schema

### Users Table (Existing)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'researcher',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Sessions Table (NEW)

```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);
```

### Messages Table (NEW)

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    message_type VARCHAR(50), -- 'text', 'analysis', 'chart'
    charts JSONB, -- Store chart data
    related_document_id INTEGER REFERENCES documents(id),
    is_regenerated BOOLEAN DEFAULT false,
    original_message_id INTEGER REFERENCES messages(id),
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_messages_user ON messages(user_id);
```

### Documents Table (NEW)

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    extracted_text TEXT,
    tables JSONB,
    content_summary TEXT,
    page_count INTEGER,
    upload_timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'processed'
);

CREATE INDEX idx_documents_user ON documents(user_id);
```

### Reports Table (NEW)

```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    generated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    download_count INTEGER DEFAULT 0
);

CREATE INDEX idx_reports_session ON reports(session_id);
CREATE INDEX idx_reports_user ON reports(user_id);
```

---

## API Endpoints Summary

### Authentication (Already Implemented)
- ✅ POST `/api/v1/auth/register`
- ✅ POST `/api/v1/auth/login`
- ✅ GET `/api/v1/auth/me`
- ✅ POST `/api/v1/auth/refresh`

### Chat & Messages (NEW - Required)
- ⭕ POST `/api/v1/chat/generate` **[PRIORITY 1]**
- ⭕ POST `/api/v1/messages`
- ⭕ GET `/api/v1/sessions/{session_id}/messages`
- ⭕ POST `/api/v1/messages/{message_id}/regenerate`

### Documents (NEW - Required)
- ⭕ POST `/api/v1/documents/upload` **[PRIORITY 2]**
- ⭕ GET `/api/v1/documents/{document_id}`
- ⭕ GET `/api/v1/documents/user/list`
- ⭕ DELETE `/api/v1/documents/{document_id}`

### Reports (NEW - Required)
- ⭕ POST `/api/v1/reports/generate` **[PRIORITY 3]**
- ⭕ GET `/api/v1/reports/{report_id}/download` **[PRIORITY 3]**

### Sessions (NEW - Optional)
- ⭕ POST `/api/v1/sessions` - Create new chat session
- ⭕ GET `/api/v1/sessions` - List user sessions
- ⭕ GET `/api/v1/sessions/{session_id}` - Get session details
- ⭕ DELETE `/api/v1/sessions/{session_id}` - Delete session

---

## Implementation Priority

### Phase 1 (Required for Basic Chat):
1. **POST `/api/v1/chat/generate`** - Core chat functionality
2. **POST `/api/v1/messages`** - Message storage
3. **GET `/api/v1/sessions/{session_id}/messages`** - Chat history

### Phase 2 (Required for PDF Features):
1. **POST `/api/v1/documents/upload`** - PDF upload
2. **GET `/api/v1/documents/{document_id}`** - Document retrieval

### Phase 3 (Report Export):
1. **POST `/api/v1/reports/generate`** - Report generation
2. **GET `/api/v1/reports/{report_id}/download`** - Report download

### Phase 4 (Enhancements):
1. **POST `/api/v1/messages/{message_id}/regenerate`** - Regenerate responses
2. **Session management endpoints**

---

## Frontend Integration Points

### API Client Location
`Client/src/utils/authApi.js` - Use this as reference for implementing new API clients

### Frontend Features Using These Endpoints

1. **ChatBox Component** (`src/components/ChatBox.jsx`):
   - Calls `POST /api/v1/chat/generate` for AI responses
   - Calls `POST /api/v1/documents/upload` for PDF upload
   - Calls `POST /api/v1/messages/{message_id}/regenerate` for regeneration

2. **Message Component** (`src/components/Message.jsx`):
   - Displays response content with markdown
   - Renders charts from response data
   - Shows download button for report export

3. **Login Component** (`src/pages/Login.jsx`):
   - Uses existing auth endpoints

4. **Sidebar Component** (`src/components/Sidebar.jsx`):
   - Manages user logout

---

## Error Handling Standards

All endpoints should return appropriate HTTP status codes:

```
200 OK - Successful request
201 Created - Resource created
400 Bad Request - Invalid input
401 Unauthorized - Missing/invalid token
403 Forbidden - Insufficient permissions
404 Not Found - Resource not found
500 Internal Server Error - Server error
```

**Error Response Format**:
```json
{
  "detail": "Error message describing what went wrong",
  "error_code": "INVALID_INPUT",
  "status": 400
}
```

---

## Testing Checklist

- [ ] User can register with valid credentials
- [ ] User can login and receive JWT tokens
- [ ] Chat generates response with markdown and charts
- [ ] PDF upload processes document correctly
- [ ] Chat history retrieves all messages
- [ ] Regenerate endpoint creates new response
- [ ] Report generates PDF with all data
- [ ] Report download returns valid PDF file
- [ ] All endpoints require authentication
- [ ] Proper error messages returned for invalid inputs

---

## Notes for Backend Developer

1. **Markdown Rendering**: The frontend uses `react-markdown` which supports GitHub-flavored markdown
2. **Chart Integration**: Charts must be Chart.js compatible JSON objects
3. **PDF Processing**: Consider using asynchronous task queue (Celery) for large files
4. **Rate Limiting**: Implement rate limiting on `/api/v1/chat/generate` to prevent abuse
5. **Token Expiration**: Implement token refresh logic (frontend already supports this)
6. **CORS**: Ensure CORS is properly configured for frontend domain
7. **Logging**: Log all API calls for debugging and monitoring
8. **Database Migrations**: Use Alembic for schema migrations
9. **Testing**: Write unit tests for all endpoints

---

**Last Updated**: December 7, 2025
**Frontend Version**: 1.0
**Backend Status**: Ready for implementation
