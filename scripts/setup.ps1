# Kilimo Credit Web - PowerShell Setup Script
# Windows + PowerShell 5.1 compatible

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Kilimo Credit Web - Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 1. Create .env from template if not exists
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[✓] Created .env from template" -ForegroundColor Green
    Write-Host "    Edit .env with your Neo4j, Featherless, and Masumi credentials" -ForegroundColor Yellow
} else {
    Write-Host "[✓] .env already exists" -ForegroundColor Cyan
}

# 2. Create Python virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "[...] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($?) {
        Write-Host "[✓] Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "[✗] Failed to create venv. Ensure Python 3.10+ is installed." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[✓] Virtual environment exists" -ForegroundColor Cyan
}

# 3. Activate and install dependencies
Write-Host "[...] Installing dependencies..." -ForegroundColor Yellow
.\.venv\Scripts\pip.exe install -r requirements.txt
if ($?) {
    Write-Host "[✓] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[✗] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# 4. Run tests
Write-Host "[...] Running tests..." -ForegroundColor Yellow
.\.venv\Scripts\pytest.exe tests/ -v
if ($?) {
    Write-Host "[✓] All tests passed" -ForegroundColor Green
} else {
    Write-Host "[!] Some tests failed (check output above)" -ForegroundColor Red
}

# 5. Run demo simulation
Write-Host "[...] Running demo simulation..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe scripts/demo_simulation.py
if ($?) {
    Write-Host "[✓] Demo simulation complete" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "  To start the API server:" -ForegroundColor Cyan
Write-Host "    .\.venv\Scripts\uvicorn.exe api.main:app --reload" -ForegroundColor White
Write-Host "  To open the frontend:" -ForegroundColor Cyan
Write-Host "    Open frontend/index.html in your browser" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Green
