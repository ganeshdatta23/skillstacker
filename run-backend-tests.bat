@echo off
echo ========================================
echo   Backend Unit Tests
echo ========================================
echo.

cd backend

echo [1/3] Setting up test environment...
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

echo [2/3] Installing test dependencies...
pip install -r requirements.txt

echo [3/3] Running tests...
pytest tests/ -v --tb=short

if %errorlevel% neq 0 (
    echo [ERROR] Some tests failed
    pause
    exit /b 1
)

echo.
echo [OK] All backend tests passed
pause