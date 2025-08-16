@echo off
echo Starting SkillStacker Full-Stack Application...
echo.

echo Starting Backend...
start "Backend" cmd /k "cd backend && uvicorn src.main:app --reload"

timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Application is starting!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
pause