Write-Host "PharmaPilot Backend Startup" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

Write-Host "[1/3] Checking Docker and PostgreSQL..." -ForegroundColor Yellow

if (Get-Command docker -ErrorAction SilentlyContinue) {
    $postgresRunning = docker ps --filter "name=postgres" --format "{{.Names}}" 2>$null
    
    if ($postgresRunning) {
        Write-Host "PostgreSQL container is running" -ForegroundColor Green
    } else {
        Write-Host "Starting PostgreSQL container..." -ForegroundColor Yellow
        docker-compose up -d postgres
        Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
} else {
    Write-Host "Docker not found. Make sure PostgreSQL is running locally." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[2/3] Checking Python dependencies..." -ForegroundColor Yellow

if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "Virtual environment not found. Using system Python." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Green
Write-Host "  - API: http://localhost:8000" -ForegroundColor White
Write-Host "  - Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - Health: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

uvicorn app.main:app --reload --port 8000