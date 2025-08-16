@echo off
title SkillStacker - Silicon Valley Grade Full-Stack Platform
color 0A

echo.
echo  ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗████████╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
echo  ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
echo  ███████╗█████╔╝ ██║██║     ██║     ███████╗   ██║   ███████║██║     █████╔╝ █████╗  ██████╔╝
echo  ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║   ██║   ██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
echo  ███████║██║  ██╗██║███████╗███████╗███████║   ██║   ██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
echo  ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
echo.
echo                          🚀 SILICON VALLEY GRADE FULL-STACK PLATFORM 🚀
echo.
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                   ENTERPRISE FEATURES                                   │
echo  ├─────────────────────────────────────────────────────────────────────────────────────────┤
echo  │  ✅ FastAPI + Next.js 14        ✅ JWT Authentication       ✅ PostgreSQL + MongoDB    │
echo  │  ✅ TypeScript + Tailwind       ✅ Docker Ready             ✅ Production Security      │
echo  │  ✅ XSS Protection              ✅ SQL Injection Prevention  ✅ Enterprise Architecture │
echo  └─────────────────────────────────────────────────────────────────────────────────────────┘
echo.

echo [INFO] Checking prerequisites...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found! Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.11+ from https://python.org/
    pause
    exit /b 1
)

echo [SUCCESS] Prerequisites check passed!
echo.

echo [INFO] Starting PostgreSQL and MongoDB (Docker)...
docker-compose up -d postgres mongodb
if %errorlevel% neq 0 (
    echo [WARNING] Docker not available. Please ensure PostgreSQL and MongoDB are running manually.
)

echo.
echo [INFO] Starting Backend (FastAPI)...
start "SkillStacker Backend" cmd /k "cd backend && echo [BACKEND] Installing dependencies... && pip install -r requirements.txt >nul 2>nul && echo [BACKEND] Starting FastAPI server... && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo [INFO] Starting Frontend (Next.js)...
start "SkillStacker Frontend" cmd /k "cd frontend && echo [FRONTEND] Installing dependencies... && npm install >nul 2>nul && echo [FRONTEND] Starting Next.js server... && npm run dev"

echo.
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                 🌐 ACCESS POINTS                                        │
echo  ├─────────────────────────────────────────────────────────────────────────────────────────┤
echo  │  🎯 Frontend Application:    http://localhost:3000                                     │
echo  │  🔧 Backend API:             http://localhost:8000                                     │
echo  │  📚 API Documentation:       http://localhost:8000/docs                               │
echo  │  📖 Alternative Docs:        http://localhost:8000/redoc                              │
echo  │  ❤️  Health Check:            http://localhost:8000/health                             │
echo  └─────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                🧪 TEST CREDENTIALS                                     │
echo  ├─────────────────────────────────────────────────────────────────────────────────────────┤
echo  │  📧 Email:    admin@skillstacker.com                                                   │
echo  │  🔑 Password: admin123                                                                  │
echo  └─────────────────────────────────────────────────────────────────────────────────────────┘
echo.

echo [SUCCESS] 🚀 SkillStacker is starting up!
echo [INFO] Both servers are launching in separate windows...
echo [INFO] Please wait 30-60 seconds for full initialization.
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:3000

echo.
echo [INFO] Application opened in browser!
echo [INFO] Check the separate terminal windows for server logs.
echo [INFO] Press Ctrl+C in each terminal to stop the servers.
echo.
pause