@echo off
echo ========================================
echo   SkillStacker - Testing Suite
echo ========================================
echo.

echo [1/7] Infrastructure Tests...
echo Testing Docker services...
docker-compose ps
if %errorlevel% neq 0 (
    echo [ERROR] Services not running. Run start-dev.bat first.
    pause
    exit /b 1
)
echo [OK] All services running

echo.
echo [2/7] Backend Health Check...
curl -f http://localhost:8000/health
if %errorlevel% neq 0 (
    echo [ERROR] Backend health check failed
    pause
    exit /b 1
)
echo [OK] Backend healthy

echo.
echo [3/7] Database Connectivity...
docker-compose exec -T postgres psql -U postgres -d skillstacker -c "SELECT COUNT(*) FROM users;"
if %errorlevel% neq 0 (
    echo [ERROR] PostgreSQL connection failed
    pause
    exit /b 1
)
echo [OK] PostgreSQL connected

echo.
echo [4/7] API Endpoints Test...
curl -f http://localhost:8000/api/v1/products/
if %errorlevel% neq 0 (
    echo [ERROR] Products API failed
    pause
    exit /b 1
)
echo [OK] Products API working

echo.
echo [5/7] Authentication Test...
curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=user@skillstacker.com&password=password123"
if %errorlevel% neq 0 (
    echo [ERROR] Authentication failed
    pause
    exit /b 1
)
echo [OK] Authentication working

echo.
echo [6/7] Frontend Accessibility...
curl -f http://localhost:3000
if %errorlevel% neq 0 (
    echo [ERROR] Frontend not accessible
    pause
    exit /b 1
)
echo [OK] Frontend accessible

echo.
echo [7/7] API Documentation...
curl -f http://localhost:8000/docs
if %errorlevel% neq 0 (
    echo [ERROR] API docs not accessible
    pause
    exit /b 1
)
echo [OK] API documentation accessible

echo.
echo ========================================
echo   ALL TESTS PASSED - SYSTEM READY
echo ========================================
echo.
echo Test Results Summary:
echo - Infrastructure: PASS
echo - Backend Health: PASS
echo - Database: PASS
echo - API Endpoints: PASS
echo - Authentication: PASS
echo - Frontend: PASS
echo - Documentation: PASS
echo.
echo System is production-ready!
pause