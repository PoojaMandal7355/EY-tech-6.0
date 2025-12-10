# PharmaPilot 🔬

> **AI-Powered Pharmaceutical Research Platform** - Transforming drug discovery with intelligent insights

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?style=flat&logo=react)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite)](https://www.sqlite.org/)

---

## About

**PharmaPilot** is an intelligent pharmaceutical research management platform designed for researchers, analysts, and pharmaceutical companies to accelerate drug discovery and market analysis. Built for **EY Technathon 6.0**, this platform combines cutting-edge AI technology with comprehensive data analytics to provide actionable insights across the pharmaceutical value chain.

### Problem We Solve

In pharmaceutical research, teams face:
- **Time-consuming manual research** across patents, trials, and market data
- **Fragmented data sources** making holistic analysis difficult  
- **Difficulty identifying opportunities** in competitive landscapes
- **Complex market analysis** requiring multiple disconnected tools

**PharmaPilot centralizes everything** - from USPTO patents to clinical trials, market intelligence to competitor analysis - in one conversational AI interface.

---

## Key Features

### **Enterprise Authentication**
- JWT-based secure authentication with automatic token refresh
- Password reset via email with time-limited tokens
- Account protection with audit logging and lockout mechanisms
- Session management and user profile tracking

### **Conversational AI Interface**
- Natural language queries for complex pharmaceutical research
- Real-time chat-based insights with markdown formatting
- Context-aware responses tailored to research needs
- Export capabilities for reports and presentations

### **Multi-Source Intelligence**
- **Patent Analysis** - USPTO patent trends, innovation tracking, technology landscapes
- **Clinical Trials** - Trial phases, success rates, therapeutic area insights  
- **Market Intelligence** - Global market sizing, growth forecasts, opportunity scoring
- **Competitor Landscape** - Company profiles, pipeline analysis, strategic positioning
- **Trade Data** - Import/export statistics, regulatory insights, market access

### **Project Management**
- Organize research by projects and therapeutic areas
- Associate molecules and compounds to specific projects
- Track project status and collaborate with teams
- User-specific project isolation for data security

---

## Architecture & Tech Stack

### Backend (FastAPI + Python)
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - Modern ORM with type safety
- **Pydantic** - Data validation and settings management
- **JWT + Bcrypt** - Secure authentication and password hashing
- **SQLite** - Embedded database (PostgreSQL-ready for production)
- **SMTP Integration** - Email service for notifications

### Frontend (React + Vite)
- **React 19** - Latest React with concurrent features
- **Vite 7** - Lightning-fast dev server and optimized builds
- **TailwindCSS 4** - Utility-first styling framework
- **React Router 7** - Client-side routing
- **Axios** - HTTP client with automatic token refresh interceptor
- **Context API** - Centralized state management

### Project Structure

\\\
PharmaPilot/
 Server/                        # FastAPI Backend
    app/
       main.py               # Application entry & CORS
       config.py             # Environment settings  
       database.py           # SQLAlchemy configuration
       models.py             # Database models
       auth.py               # JWT & password utilities
       email_service.py      # Gmail SMTP service
       routes/               # API endpoints
    requirements.txt

 Client/                        # React Frontend
    src/
       pages/                # Page components
       components/           # Reusable UI components
       utils/                # API clients & utilities
       context/              # Global state management
    package.json

 Data/                          # Research datasets
     uspto_patents_detailed.json
     clinical_trials_mock.json
     ...
\\\

---

## Quick Start

### Prerequisites
- **Python 3.9+**  [Download](https://www.python.org/downloads/)
- **Node.js 18+**  [Download](https://nodejs.org/)
- **Git**  [Download](https://git-scm.com/)

### Installation

**1. Clone the Repository**
\\\ash
git clone https://github.com/PoojaMandal7355/EY-tech-6.0.git
cd EY-tech-6.0
\\\

**2. Setup Backend**
\\\ash
cd Server
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# Create .env file with required configuration (see Configuration section)

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
\\\
Backend  **http://localhost:8000**

**3. Setup Frontend**
\\\ash
cd Client
npm install

# Create .env file: VITE_API_URL=http://localhost:8000/api/v1

npm run dev
\\\
Frontend  **http://localhost:5173**

### Configuration

**Backend \.env\ (Server/.env)**
\\\env
DATABASE_URL=sqlite:///./pharmapilot.db
SECRET_KEY=your-secret-key-here
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:5173
FRONTEND_URL=http://localhost:5173

# Optional: Email service for password reset
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
\\\

**Frontend \.env\ (Client/.env)**
\\\env
VITE_API_URL=http://localhost:8000/api/v1
\\\

---

## How It Works

1. **Register/Login** - Create an account or login with existing credentials
2. **Create Projects** - Organize research by therapeutic areas and compounds
3. **Ask Questions** - Use natural language to query pharmaceutical data:
   - *"Latest oncology patent trends?"*
   - *"Phase 3 cardiovascular trial success rates"*
   - *"Competitor landscape in immunotherapy"*
4. **Get Insights** - Receive comprehensive analysis, charts, and recommendations

---

## API Overview

Interactive docs: **http://localhost:8000/docs**

**Authentication**
\\\
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/forgot-password
POST /api/v1/auth/reset-password
\\\

**Projects**
\\\
GET    /api/v1/projects
POST   /api/v1/projects
PUT    /api/v1/projects/{id}
DELETE /api/v1/projects/{id}
\\\

**Chat & AI**
\\\
POST /api/v1/chat/generate
\\\

---

## Current Status

**Complete**
- Enterprise authentication with JWT & token refresh
- Password reset via email
- Project management (full CRUD)
- Chat interface with mock responses
- Responsive UI design
- API documentation

**In Progress**
- LangGraph AI agents integration
- Real-time data connectors
- Advanced analytics dashboard

---

## Team

**PharmaPilot** - Made with ❤️ by **MindOrbit** for EY Technathon 6.0

**Repository:** [github.com/PoojaMandal7355/EY-tech-6.0](https://github.com/PoojaMandal7355/EY-tech-6.0)

---

## License

Developed by MindOrbit for EY Technathon 6.0

---

<div align='center'>

**Accelerating Discovery | Empowering Researchers | Transforming Healthcare**

</div>
