# PharmaPilot 🔬

> AI-powered pharmaceutical research platform for patent analysis, market intelligence, and competitive insights.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?style=flat&logo=react)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite)](https://www.sqlite.org/)

## 🌟 What is PharmaPilot?

PharmaPilot is a comprehensive pharmaceutical research management platform that helps researchers:
- 🔍 Analyze patent trends and innovations
- 📊 Track market intelligence and opportunities
- 🏢 Monitor competitor landscapes
- 🧪 Access clinical trial insights
- 🌍 Review global trade dynamics

## 🚀 Quick Start (5 Minutes)

### Prerequisites
Make sure you have these installed on your system:
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/downloads)

### Step 1: Clone the Repository
```bash
git clone https://github.com/PoojaMandal7355/EY-tech-6.0.git
cd EY-tech-6.0
```

### Step 2: Set Up the Backend (API)

```bash
# Navigate to Server folder
cd Server

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
# Create a file named .env in the Server/ directory and add:
# DATABASE_URL=sqlite:///./pharmapilot.db
# SECRET_KEY=your-secret-key-change-in-production
# API_V1_PREFIX=/api/v1
# CORS_ORIGINS=http://localhost:5173
# FRONTEND_URL=http://localhost:5173
# GMAIL_EMAIL=your-gmail@gmail.com
# GMAIL_APP_PASSWORD=your-16-char-app-password

# Start the backend server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The backend will start at **http://localhost:8000** ✅

### Step 3: Set Up the Frontend (UI)

Open a **new terminal window** and run:

```bash
# Navigate to frontend folder
cd Client

# Install dependencies
npm install

# Create environment file
# Create a file named .env in the Client/ directory and add:
# VITE_API_URL=http://localhost:8000/api/v1
# Note: .env is in .gitignore for security

# Start the development server
npm run dev
```

The frontend will start at **http://localhost:5173** ✅

### Step 4: Access the Application

Open your browser and visit:
- 🎨 **Frontend UI:** http://localhost:5173
- 🔧 **API Docs:** http://localhost:8000/docs
- ✅ **Health Check:** http://localhost:8000/health

**That's it! You're ready to go! 🎉**

## 📁 Project Structure

```
PharmaPilot/
├── 📂 Server/                     # FastAPI Backend API
│   ├── 📂 app/
│   │   ├── __init__.py           # Package initializer
│   │   ├── main.py               # Application entry point & CORS setup
│   │   ├── config.py             # Environment configuration (Pydantic settings)
│   │   ├── database.py           # Database connection & session management
│   │   ├── models.py             # SQLAlchemy ORM models (User, Project, etc.)
│   │   ├── auth.py               # JWT token utilities & password hashing
│   │   ├── email_service.py      # Gmail SMTP service for password resets
│   │   └── 📂 routes/
│   │       ├── __init__.py       # Routes package
│   │       ├── auth.py           # Auth endpoints (login, register, forgot-password)
│   │       ├── projects.py       # Project CRUD endpoints
│   │       └── chat.py           # Chat & AI response endpoints
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables (SECRET_KEY, GMAIL_*, etc.)
│   ├── .gitignore                # Git ignore rules
│   └── pharmapilot.db           # SQLite database (auto-created)
│
├── 📂 Client/                     # React + Vite Frontend
│   ├── 📂 public/                # Static assets
│   ├── 📂 src/
│   │   ├── 📂 pages/
│   │   │   ├── Login.jsx         # Login & Register page
│   │   │   ├── ResetPassword.jsx # Password reset form
│   │   │   ├── Home.jsx          # Main dashboard
│   │   │   └── Loading.jsx       # Loading screen
│   │   ├── 📂 components/
│   │   │   ├── ChatBox.jsx       # Chat interface
│   │   │   ├── Sidebar.jsx       # Navigation sidebar
│   │   │   ├── Message.jsx       # Chat message component
│   │   │   ├── NavBar.jsx        # Top navigation
│   │   │   ├── Hero.jsx          # Landing hero section
│   │   │   ├── StatsSection.jsx  # Statistics display
│   │   │   └── ...               # Other UI components
│   │   ├── 📂 context/
│   │   │   └── AppContext.jsx    # Global state (auth, projects, messages)
│   │   ├── 📂 utils/
│   │   │   ├── authApi.js        # Authentication API calls
│   │   │   ├── projectsApi.js    # Projects API client
│   │   │   ├── agentsApi.js      # Agents API client
│   │   │   ├── fetchInterceptor.js # Axios interceptor for token refresh
│   │   │   ├── responseGenerator.js # Mock/AI chat responses
│   │   │   └── typingAnimation.js # Typing effect utility
│   │   ├── 📂 styles/
│   │   │   └── ...               # CSS modules
│   │   ├── 📂 assets/
│   │   │   └── assets.js         # Image/icon imports
│   │   ├── App.jsx               # Root component & routing
│   │   ├── main.jsx              # React entry point
│   │   └── index.css             # Global styles (Tailwind)
│   ├── package.json              # Node dependencies
│   ├── package-lock.json         # Locked dependency versions
│   ├── .env                      # Frontend config (VITE_API_URL)
│   ├── .env.example              # Example environment file
│   ├── .gitignore                # Git ignore (.env, node_modules, etc.)
│   ├── vite.config.js            # Vite build configuration
│   ├── eslint.config.js          # ESLint rules
│   └── index.html                # HTML entry point
│
├── 📂 Data Files/                 # Mock/Research datasets
│   ├── class_trends.json         # Drug class trends
│   ├── clinical_trials_mock.json # Clinical trial data
│   ├── competitor_landscape.json # Competitor analysis
│   ├── exim_data.json            # Export/import statistics
│   ├── market_overview.json      # Market intelligence
│   ├── opportunity_score.json    # Opportunity scoring
│   └── uspto_patents_detailed.json # USPTO patent data
│
└── README.md                      # Project documentation (you are here!)
```

## 💡 How to Use PharmaPilot

### 1. Create an Account
- Open http://localhost:5173
- Click "Sign Up" tab
- Enter your details (email, name, password)
- Password must be 8+ characters with uppercase, lowercase, and digit
- Click "Register"

### 2. Login
- Use your email and password
- You'll be redirected to the main dashboard
- If you forget your password, click "Forgot Password?" to receive a reset email

### 3. Ask Questions
Type any pharmaceutical research question in the chat:
- "What are the latest patent trends in oncology?"
- "Show me market analysis for cardiovascular drugs"
- "Analyze competitor landscape in immunology"
- "Clinical trial success rates by phase"
- "Export data for Indian pharmaceutical companies"

### 4. Get AI-Powered Insights
The system will provide:
- 📄 Detailed analysis and reports
- 📊 Visual charts and graphs
- 🔍 Key insights and recommendations
- 📈 Trend analysis

## 🔑 Key Features

### ✨ Authentication & Security (Production-Ready)
- ✅ Secure user registration and login
- 🔐 JWT token-based authentication with refresh tokens
- 🔄 Automatic token refresh via interceptor
- 🛡️ Password hashing with bcrypt
- 👤 User profile management
- 🔒 **Account lockout** after 5 failed attempts
- 📊 **Audit logging** for all auth events
- 💪 **Strong password** enforcement (8+ chars, upper/lower/digit)
- 🕐 **Last login tracking**
- 🔑 **Forgot password** workflow with secure email tokens (30-min expiry)
- 📧 **Email service** via Gmail SMTP for password reset links

### 📋 Project Management
- ➕ Create research projects
- 📝 Edit project details
- 🗑️ Delete projects
- 📊 Track project status
- 🔬 Associate molecules with projects

### 🤖 AI-Powered Research
- **Patent Analysis** - USPTO data and innovation trends
- **Market Intelligence** - Global market size and growth projections
- **Competitor Analysis** - Company profiles and competitive landscape
- **Clinical Trials** - Trial phases, success rates, and insights
- **Trade Data** - Export/import statistics and opportunities

### 💬 Interactive Chat Interface
- Real-time conversational AI
- Context-aware responses
- Chart visualizations
- Markdown-formatted answers
- Copy and export capabilities

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.100+ | Web framework & API |
| SQLAlchemy | 2.0 | ORM for database |
| SQLite | 3 | Database (development) |
| Pydantic | 2.0+ | Data validation & settings |
| JWT (PyJWT) | - | Authentication tokens |
| Bcrypt | 4.1.2 | Password hashing |
| Uvicorn | 0.23 | ASGI server |
| Python-JOSE | - | JWT encoding/decoding |
| Passlib | - | Password utilities |
| Python-Multipart | - | Form data parsing |
| Email-Validator | - | Email validation |
| SMTP (Gmail) | - | Password reset emails |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.0 | UI framework |
| Vite | 7.2.6 | Build tool & dev server |
| TailwindCSS | 4.1.17 | Utility-first CSS |
| React Router | 7.10.1 | Client-side routing |
| Axios | 1.7+ | HTTP client & interceptors |
| Context API | - | Global state management |
| Framer Motion | - | Animations |
| React Markdown | - | Markdown rendering |

## 📚 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Main Endpoints

#### Authentication
```
POST /api/v1/auth/register           # Create new account
POST /api/v1/auth/login              # Login to get tokens
GET  /api/v1/auth/me                 # Get current user info
POST /api/v1/auth/refresh            # Refresh access token
POST /api/v1/auth/forgot-password    # Request password reset email
POST /api/v1/auth/reset-password     # Reset password with token
```

#### Projects
```
GET    /api/v1/projects       # List all projects
POST   /api/v1/projects       # Create new project
GET    /api/v1/projects/{id}  # Get project details
PUT    /api/v1/projects/{id}  # Update project
DELETE /api/v1/projects/{id}  # Delete project
```

#### Chat & Research
```
POST /api/v1/chat/generate    # Get AI research insights
GET  /api/v1/agents/logs      # View agent execution history
```

## ⚙️ Configuration

### Backend Environment Variables

Create a file `Server/.env`:

```env
# Database (SQLite for development)
DATABASE_URL=sqlite:///./pharmapilot.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256

# Token Settings
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Settings
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Frontend URL (for password reset emails)
FRONTEND_URL=http://localhost:5173

# Email Service (Gmail SMTP for password resets)
GMAIL_EMAIL=your-gmail@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

> **Note:** To get a Gmail App Password:
> 1. Enable 2-factor authentication on your Google account
> 2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
> 3. Generate a new app password for "Mail"
> 4. Copy the 16-character password to `GMAIL_APP_PASSWORD`

### Frontend Environment Variables

Create a file `Client/.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🐛 Troubleshooting

### Backend Not Starting

**Problem:** `ModuleNotFoundError` or import errors
```bash
# Solution: Reinstall dependencies
cd Server
pip install -r requirements.txt
```

**Problem:** `bcrypt` version error
```bash
# Solution: Install specific bcrypt version
pip install "bcrypt==4.1.2"
```

**Problem:** Port 8000 already in use
```bash
# Solution: Kill the process or use different port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Or run on different port:
uvicorn app.main:app --port 8001
```

### Frontend Not Starting

**Problem:** `npm install` fails
```bash
# Solution: Clear cache and reinstall
cd Client
rm -rf node_modules package-lock.json
npm install
```

**Problem:** Can't connect to backend
- ✅ Verify backend is running on http://localhost:8000
- ✅ Check `VITE_API_URL` in `Client/.env`
- ✅ Open browser console for error details

### Authentication Issues

**Problem:** Login fails or "Invalid credentials"
- ✅ Make sure you registered first at `/register`
- ✅ Check backend logs for errors
- ✅ Verify database file exists: `Server/pharmapilot.db`

**Problem:** "Token expired" errors
- ✅ This is normal after 30 minutes
- ✅ Tokens auto-refresh via interceptor; if that fails, login again

**Problem:** Password reset email not received
- ✅ Check spam/junk folder
- ✅ Verify `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD` in `Server/.env`
- ✅ Ensure 2FA is enabled on Gmail account
- ✅ Check backend logs for SMTP errors
- ✅ Token expires in 30 minutes

**Problem:** "Failed to send reset email"
- ✅ Verify Gmail App Password is correct (16 chars, no spaces)
- ✅ Test email service: `cd Server; python test_email_service.py`
- ✅ Check if Gmail SMTP is blocked by firewall

### Database Issues

**Problem:** Database errors or missing tables
```bash
# Solution: Delete and recreate database
cd Server
rm pharmapilot.db
# Restart backend - tables will be created automatically
```

## 🚢 Deployment

### Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update `CORS_ORIGINS` to your production domains
- [ ] Use PostgreSQL instead of SQLite for production
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Review security settings

### Backend Deployment Options

**Option 1: Railway / Render / Fly.io**
```bash
# These platforms support Python apps out of the box
# Just connect your GitHub repo and deploy!
```

**Option 2: Docker**
```bash
cd Server
docker build -t pharmapilot-backend .
docker run -p 8000:8000 pharmapilot-backend
```

### Frontend Deployment Options

**Option 1: Vercel (Recommended)**
```bash
cd Client
npm install -g vercel
vercel --prod
```

**Option 2: Netlify**
```bash
cd Client
npm run build
# Upload dist/ folder to Netlify
```

**Option 3: GitHub Pages**
```bash
cd Client
npm run build
# Deploy dist/ folder to gh-pages branch
```

## 📖 Additional Documentation

For more detailed information:

- 📘 **[Backend Documentation](./Server/README_BACKEND.md)** - Complete backend setup guide
- 🏗️ **[Architecture](./Server/ARCHITECTURE.md)** - System architecture and design
- 🔌 **[API Integration](./Server/API_INTEGRATION.md)** - Comprehensive API reference

> **Note:** Interactive API documentation is also available at http://localhost:8000/docs when the backend is running.

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

## 📝 License

This project is developed for EY Technathon 6.0.

## 👥 Team & Support

- **Project:** PharmaPilot - AI-Powered Pharmaceutical Research Platform
- **Built for:** EY Technathon 6.0
- **Repository:** [github.com/PoojaMandal7355/EY-tech-6.0](https://github.com/PoojaMandal7355/EY-tech-6.0)

### Need Help?

- 📖 Check the [Backend Documentation](./Server/README_BACKEND.md)
- 🏗️ Review the [Architecture Guide](./Server/ARCHITECTURE.md)
- 🔍 Browse the [API Reference](./Server/API_INTEGRATION.md)
- 📄 View interactive API docs at http://localhost:8000/docs
- 🐛 Open an issue on GitHub
- 📧 Contact the development team

## 🎯 Project Status & Features

✅ **Authentication & Security** - **Production-ready**
   - User registration & login with JWT tokens
   - Token auto-refresh via Axios interceptor
   - Forgot password workflow with email service
   - Password reset tokens (30-min expiry)
   - Account lockout after 5 failed attempts
   - Audit logging for security events
   - Strong password enforcement
   - Last login tracking

✅ **Project Management** - Fully implemented
   - Create, read, update, delete projects
   - Project status tracking
   - Molecule association
   - User-specific project isolation

✅ **Chat Interface** - Working with mock data
   - Real-time conversational UI
   - Context-aware responses
   - Markdown rendering
   - Copy & export capabilities

✅ **Email Service** - Gmail SMTP integration
   - Password reset emails
   - Secure token generation
   - HTML email templates

✅ **Frontend Features**
   - Responsive design with TailwindCSS
   - Token refresh interceptor
   - Global state management via Context API
   - Protected routes & auth guards
   - Loading states & error handling

⏳ **AI Insights** - Mock responses active (ready for LangGraph integration)  
⏳ **Production Database** - SQLite (upgrade to PostgreSQL recommended)  

---

Made with ❤️ for pharmaceutical research innovation

**Happy Coding! 🚀**

