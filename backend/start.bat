@echo off
echo ========================================
echo PharmaPilot Backend - Quick Start
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)
echo Python found!

REM Check Docker
echo Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not found!
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo Docker found!

REM Create virtual environment
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python packages...
pip install -q -r requirements.txt
echo Dependencies installed!

REM Start Docker database
echo.
echo Starting PostgreSQL database...
docker-compose up -d
timeout /t 5 /nobreak >nul
echo Database started!

REM Show status
echo.
echo ========================================
echo Backend is ready to start!
echo ========================================
echo.
echo Starting FastAPI server...
echo.
echo API will be available at:
echo   http://localhost:8000
echo   http://localhost:8000/docs (API documentation)
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start FastAPI
uvicorn app.main:app --reload --port 8000
