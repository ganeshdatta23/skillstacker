# 🚀 SkillStacker - Quick Reference Guide

## 📋 Essential Commands

### Start the Application
```bash
# Using Docker (Recommended)
docker-compose up -d

# Manual Setup
cd backend && uvicorn src.main:app --reload
cd frontend && npm run dev
```

### Test CRUD Operations
```bash
cd backend
python test_crud_operations.py
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database Admin**: http://localhost:8080 (if using pgAdmin)

## 🔧 API Endpoints Quick Reference

### Films (PostgreSQL)
```http
POST   /unified/films           # Create film
GET    /unified/films/{id}      # Get film
PUT    /unified/films/{id}      # Update film
DELETE /unified/films/{id}      # Delete film
```

### Actors (PostgreSQL)
```http
POST   /unified/actors          # Create actor
GET    /unified/actors/{id}     # Get actor
PUT    /unified/actors/{id}     # Update actor
DELETE /unified/actors/{id}     # Delete actor
```

### Reviews (MongoDB)
```http
POST   /unified/reviews         # Create review
GET    /unified/reviews/{id}    # Get review
PUT    /unified/reviews/{id}    # Update review
DELETE /unified/reviews/{id}    # Delete review
```

### Search & Analytics
```http
GET    /unified/search          # Search all data
GET    /unified/stats           # Get statistics
GET    /unified/categories      # Get categories
```

### Bulk Operations
```http
POST   /unified/bulk/films      # Bulk create films
POST   /unified/bulk/reviews    # Bulk create reviews
```

## 💻 Code Examples

### Create a Film
```bash
curl -X POST "http://localhost:8000/unified/films" \
  -d "title=My Movie&description=Great film&rating=PG-13"
```

### Search Everything
```bash
curl "http://localhost:8000/unified/search?q=action&limit=10"
```

### Get Statistics
```bash
curl "http://localhost:8000/unified/stats"
```

## 🗂️ Project Structure
```
skillstacker/
├── backend/src/api/unified_data.py  # Main CRUD API
├── backend/test_crud_operations.py  # Test suite
├── frontend/src/app/               # Next.js pages
├── COMPLETE_PROJECT_GUIDE.md       # Beginner guide
├── API_DOCUMENTATION.md            # Complete API docs
└── README.md                       # Main documentation
```

## 🐛 Common Issues & Solutions

### "Connection refused"
```bash
# Check if services are running
docker-compose ps
# Restart if needed
docker-compose restart
```

### "Module not found"
```bash
# Backend
cd backend && pip install -r requirements.txt
# Frontend
cd frontend && npm install
```

### "Database not found"
```bash
# Reset databases
docker-compose down -v
docker-compose up -d
```

## 📚 Documentation Links

- **[Complete Beginner's Guide](./COMPLETE_PROJECT_GUIDE.md)** - Start here if new
- **[API Documentation](./API_DOCUMENTATION.md)** - Complete API reference
- **[CRUD Operations](./backend/CRUD_OPERATIONS.md)** - Database operations guide
- **[Interactive API Docs](http://localhost:8000/docs)** - Test APIs in browser

## 🎯 Learning Path

1. **Read** [Complete Beginner's Guide](./COMPLETE_PROJECT_GUIDE.md)
2. **Setup** development environment
3. **Run** `python test_crud_operations.py`
4. **Explore** http://localhost:8000/docs
5. **Build** your own features

## 🔑 Key Concepts

- **CRUD**: Create, Read, Update, Delete operations
- **PostgreSQL**: Structured data (films, actors, users)
- **MongoDB**: Flexible data (reviews, publications)
- **FastAPI**: Python web framework for APIs
- **Next.js**: React framework for frontend
- **Docker**: Containerization for easy deployment

---

**Need help?** Check the [Complete Beginner's Guide](./COMPLETE_PROJECT_GUIDE.md) or [API Documentation](./API_DOCUMENTATION.md)!