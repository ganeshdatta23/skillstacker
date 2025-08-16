@echo off
color 0A
echo ========================================
echo   SkillStacker - Enterprise Platform
echo ========================================
echo.

echo [1/4] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found. Install Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is ready

echo [2/4] Starting services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)

echo [3/4] Waiting for services to initialize...
timeout /t 10 /nobreak >nul

echo [4/4] Services ready!
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo Demo Login: user@skillstacker.com / password123
echo Admin:      admin@skillstacker.com / password123
echo.
echo Press ENTER to view logs or CTRL+C to exit...
pause >nul

docker-compose logs -f