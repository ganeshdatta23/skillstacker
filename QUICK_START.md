# SkillStacker Quick Start

## Setup & Run

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Test Everything

### Backend Test
```bash
python test_backend.py
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Demo Accounts
- **User**: demo@skillstacker.com / demo123
- **Admin**: admin@skillstacker.com / admin123

## Database
- **Type**: SQLite (skillstacker.db)
- **Location**: backend/skillstacker.db
- **Sample Data**: 4 products, 2 users

## Key Features Working
✅ User authentication (JWT)
✅ Product catalog with search
✅ User dashboard
✅ SQLite database with sample data
✅ CORS configured for frontend
✅ Error handling with fallback data

## Architecture
```
backend/
├── src/
│   ├── main.py          # FastAPI app
│   ├── api/             # API routes
│   ├── db/              # Database models
│   └── core/            # Configuration
├── init_db.py           # Database setup
└── skillstacker.db      # SQLite database

frontend/
├── src/app/
│   ├── page.tsx         # Homepage
│   ├── login/           # Login page
│   ├── products/        # Products page
│   └── dashboard/       # Dashboard
└── package.json
```