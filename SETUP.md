# SkillStacker Quick Setup Guide

## Prerequisites

- Docker Desktop installed and running
- Git (optional, for cloning)

## Quick Start (Docker - Recommended)

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd skillstacker
   ```

2. **Start all services**
   ```bash
   # Windows
   start-dev.bat
   
   # Linux/Mac
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Demo Login Credentials**
   - Regular User: `user@skillstacker.com` / `password123`
   - Admin User: `admin@skillstacker.com` / `password123`

## Manual Development Setup

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Database Setup
- PostgreSQL: localhost:5432 (postgres/postgres)
- MongoDB: localhost:27017 (mongo/mongo)

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database connection**: Ensure Docker containers are running
3. **CORS errors**: Check API_URL in frontend/.env.local

## Project Structure

```
skillstacker/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── db/              # Database initialization
├── docker-compose.yml
└── README.md
```

## Features Implemented

✅ User authentication (JWT)
✅ Product catalog with PostgreSQL
✅ Reviews system with MongoDB
✅ User dashboard
✅ Admin functionality
✅ Responsive design
✅ Docker containerization
✅ API documentation
✅ Basic testing setup