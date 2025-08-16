@echo off
echo Starting SkillStacker...

echo.
echo Initializing database...
cd backend
python init_db.py

echo.
echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo.
echo Demo accounts:
echo User: demo@skillstacker.com / demo123
echo Admin: admin@skillstacker.com / admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000