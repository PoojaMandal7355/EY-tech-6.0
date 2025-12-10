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
# Create a file named .env and add:
# DATABASE_URL=sqlite:///./pharmapilot.db
# SECRET_KEY=your-secret-key-change-in-production
# API_V1_PREFIX=/api/v1
# CORS_ORIGINS=http://localhost:5173

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
# Create a file named .env and add:
# VITE_API_URL=http://localhost:8000/api/v1

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
│   │   ├── main.py               # Application entry point
│   │   ├── config.py             # Configuration settings
│   │   ├── database.py           # Database connection
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── auth.py               # JWT authentication
│   │   └── 📂 routes/
│   │       ├── auth.py           # Login/Register endpoints
│   │       ├── projects.py       # Project CRUD endpoints
│   │       ├── agents.py         # AI agent endpoints
│   │       └── chat.py           # Chat response endpoints
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   └── pharmapilot.db           # SQLite database
│
├── 📂 Client/                     # React Frontend
│   ├── 📂 src/
│   │   ├── 📂 pages/
│   │   │   ├── Login.jsx         # Authentication page
│   │   │   ├── Home.jsx          # Main dashboard
│   │   │   └── Loading.jsx       # Loading screen
│   │   ├── 📂 components/
│   │   │   ├── ChatBox.jsx       # Chat interface
│   │   │   ├── Sidebar.jsx       # Navigation sidebar
│   │   │   └── ...               # Other UI components
│   │   ├── 📂 context/
│   │   │   └── AppContext.jsx    # Global state management
│   │   └── 📂 utils/
│   │       ├── authApi.js        # Authentication API client
│   │       ├── projectsApi.js    # Projects API client
│   │       ├── agentsApi.js      # Agents API client
│   │       └── responseGenerator.js # Chat responses
│   ├── package.json              # Node dependencies
│   ├── .env                      # Frontend config
│   └── vite.config.js            # Vite build config
│
└── README.md                      # You are here!
```

## 💡 How to Use PharmaPilot

### 1. Create an Account
- Open http://localhost:5173
- Click "Sign Up"
- Enter your details (email, name, password)
- Click "Register"

### 2. Login
- Use your email and password
- You'll be redirected to the main dashboard

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
- 🔐 JWT token-based authentication
- 🔄 Automatic token refresh
- 🛡️ Password hashing with bcrypt
- 👤 User profile management
- 🔒 **Account lockout** after 5 failed attempts
- 📊 **Audit logging** for all auth events
- 💪 **Strong password** enforcement
- 🕐 **Last login tracking**
- 🔑 **Forgot password** workflow with secure tokens

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
| FastAPI | 0.100+ | Web framework |
| SQLAlchemy | 2.0 | ORM for database |
| SQLite | 3 | Database (development) |
| JWT | - | Authentication tokens |
| Bcrypt | 4.1.2 | Password hashing |
| Uvicorn | 0.23 | ASGI server |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.0 | UI framework |
| Vite | 7.2.6 | Build tool |
| TailwindCSS | 4.1.17 | Styling |
| React Router | 7.10.1 | Routing |
| Axios | - | HTTP client |

## 📚 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Main Endpoints

#### Authentication
```
POST /api/v1/auth/register    # Create new account
POST /api/v1/auth/login       # Login to get tokens
GET  /api/v1/auth/me          # Get current user info
POST /api/v1/auth/refresh     # Refresh access token
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
```

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
- ✅ Just login again to get new tokens

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

## 🎯 Project Status

✅ **Authentication** - **Production-ready** with account lockout, audit logging, strong passwords, forgot password workflow  
✅ **Project Management** - Fully implemented  
✅ **Chat Interface** - Working with mock data  
✅ **AI Insights** - Mock responses active  
⏳ **LangGraph Agents** - Ready for integration (see agents folder structure)  
⏳ **Production Database** - SQLite (upgrade to PostgreSQL for production)  

> 🔒 **Security Docs:** [`PRODUCTION_READY.md`](./PRODUCTION_READY.md) | [`AUTHENTICATION_SUMMARY.md`](./AUTHENTICATION_SUMMARY.md) | [`FORGOT_PASSWORD.md`](./FORGOT_PASSWORD.md)  

---

Made with ❤️ for pharmaceutical research innovation

**Happy Coding! 🚀**

