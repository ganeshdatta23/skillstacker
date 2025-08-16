# 📚 SkillStacker - Complete Beginner's Guide

Welcome to SkillStacker! This guide will help you understand everything about this project, even if you're new to programming. We'll explain concepts in simple terms and show you how everything works together.

## 🎯 What is SkillStacker?

SkillStacker is a **full-stack web application** - think of it like a complete website with both:
- **Frontend**: What users see and interact with (like a store website)
- **Backend**: The server that handles data and business logic (like the warehouse and cashier)

It's designed to showcase modern web development practices and can be used as a learning platform or adapted for real business needs.

## 🏗️ Project Architecture (The Big Picture)

```
SkillStacker Project
├── Frontend (Next.js) - The User Interface
│   ├── Pages (what users see)
│   ├── Components (reusable UI pieces)
│   └── Styles (how it looks)
├── Backend (FastAPI) - The Server
│   ├── API Endpoints (how frontend talks to backend)
│   ├── Database Models (data structure)
│   └── Business Logic (rules and processing)
└── Databases - Data Storage
    ├── PostgreSQL (structured data like users, products)
    └── MongoDB (flexible data like reviews, articles)
```

## 🔧 Technologies Used (And Why)

### **Frontend Technologies**
- **Next.js 14**: A React framework that makes building websites easier
  - *Why?* Provides server-side rendering, routing, and optimization out of the box
- **TypeScript**: JavaScript with type checking
  - *Why?* Catches errors before they happen, makes code more reliable
- **Tailwind CSS**: Utility-first CSS framework
  - *Why?* Faster styling, consistent design, responsive by default

### **Backend Technologies**
- **FastAPI**: Modern Python web framework
  - *Why?* Fast, automatic API documentation, type hints support
- **PostgreSQL**: Relational database
  - *Why?* ACID compliance, complex queries, data integrity
- **MongoDB**: Document database
  - *Why?* Flexible schema, good for varied data structures
- **SQLAlchemy**: Python SQL toolkit and ORM
  - *Why?* Database abstraction, prevents SQL injection

### **DevOps & Tools**
- **Docker**: Containerization platform
  - *Why?* Consistent environments, easy deployment
- **GitHub Actions**: CI/CD pipeline
  - *Why?* Automated testing and deployment

## 📁 Project Structure Explained

### **Backend Structure**
```
backend/
├── src/                    # Source code
│   ├── api/               # API endpoints (routes)
│   │   ├── auth.py        # User login/registration
│   │   ├── films.py       # Movie operations
│   │   ├── actors.py      # Actor operations
│   │   ├── reviews.py     # Review system
│   │   └── unified_data.py # Combined operations
│   ├── core/              # Core functionality
│   │   ├── config.py      # App settings
│   │   ├── security.py    # Password hashing, JWT
│   │   └── dependencies.py # Shared dependencies
│   ├── db/                # Database related
│   │   ├── models.py      # PostgreSQL table definitions
│   │   ├── mongo_models.py # MongoDB document definitions
│   │   └── postgres.py    # Database connection
│   ├── services/          # Business logic
│   └── schemas.py         # Data validation rules
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
└── Dockerfile            # Container configuration
```

### **Frontend Structure**
```
frontend/
├── src/
│   ├── app/              # Next.js 14 App Router
│   │   ├── page.tsx      # Homepage
│   │   ├── login/        # Login page
│   │   ├── products/     # Product catalog
│   │   └── dashboard/    # User dashboard
│   ├── components/       # Reusable UI components
│   │   ├── Header.tsx    # Navigation bar
│   │   ├── ProductCard.tsx # Product display
│   │   └── LoginForm.tsx # Login form
│   ├── contexts/         # Global state management
│   └── lib/             # Utility functions
├── public/              # Static files (images, icons)
├── package.json         # Node.js dependencies
└── Dockerfile          # Container configuration
```

## 🗄️ Database Design

### **PostgreSQL Tables** (Structured Data)
```sql
-- Users table: Store user information
users (
    customer_id,     -- Unique user ID
    first_name,      -- User's first name
    last_name,       -- User's last name
    email,           -- Login email
    password_hash,   -- Encrypted password
    is_admin,        -- Admin privileges
    created_at       -- When account was created
)

-- Films table: Store movie information
films (
    film_id,         -- Unique film ID
    title,           -- Movie title
    description,     -- Movie description
    release_year,    -- Year released
    rental_rate,     -- Cost to rent
    length,          -- Duration in minutes
    rating           -- Age rating (G, PG, R, etc.)
)

-- Actors table: Store actor information
actors (
    actor_id,        -- Unique actor ID
    first_name,      -- Actor's first name
    last_name        -- Actor's last name
)
```

### **MongoDB Collections** (Flexible Data)
```javascript
// Reviews collection: Store user reviews
{
    _id: ObjectId,           // Unique review ID
    title: "Great movie!",   // Review title
    content: "I loved...",   // Review text
    rating: 5,               // 1-5 star rating
    user_id: 123,           // Who wrote it
    product_id: 456,        // What it's about
    created_at: Date,       // When written
    updated_at: Date        // Last modified
}

// Publications collection: Store articles/blogs
{
    _id: ObjectId,
    title: "Article Title",
    content: "Article content...",
    type: "blog",
    groups: ["tech", "programming"],
    published_at: Date
}
```

## 🔄 How Data Flows (Request Lifecycle)

Let's trace what happens when a user searches for a movie:

1. **User Action**: User types "action" in search box and clicks search
2. **Frontend**: React component sends HTTP request to backend
3. **Backend Routing**: FastAPI receives request at `/unified/search?q=action`
4. **Authentication**: Middleware checks if user is logged in (if required)
5. **Input Validation**: System cleans and validates the search term
6. **Database Query**: 
   - PostgreSQL: Search films table for titles containing "action"
   - MongoDB: Search reviews collection for "action" in content
7. **Data Processing**: Combine results from both databases
8. **Response**: Send JSON response back to frontend
9. **UI Update**: Frontend displays search results to user

## 🔐 Security Features

### **Authentication & Authorization**
```python
# How user login works:
1. User submits email/password
2. Backend verifies password against hashed version
3. If valid, create JWT token
4. Token sent back to frontend
5. Frontend includes token in future requests
6. Backend validates token for protected routes
```

### **Data Protection**
- **Password Hashing**: Passwords never stored in plain text
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Input sanitization
- **CORS Configuration**: Controls which domains can access API

## 🚀 API Endpoints Explained

### **Authentication Endpoints**
```http
POST /api/v1/auth/register
# Creates new user account
# Body: {"email": "user@example.com", "password": "secure123", "first_name": "John", "last_name": "Doe"}

POST /api/v1/auth/login
# Logs in existing user
# Body: {"email": "user@example.com", "password": "secure123"}
# Returns: JWT token for future requests
```

### **CRUD Endpoints** (Create, Read, Update, Delete)
```http
# Films
POST /unified/films          # Create new film
GET /unified/films/123       # Get specific film
PUT /unified/films/123       # Update film
DELETE /unified/films/123    # Delete film

# Reviews
POST /unified/reviews        # Create new review
GET /unified/reviews/abc123  # Get specific review
PUT /unified/reviews/abc123  # Update review
DELETE /unified/reviews/abc123 # Delete review
```

### **Search & Analytics**
```http
GET /unified/search?q=action&category=films&limit=10
# Search across all data sources
# Returns: Combined results from PostgreSQL and MongoDB

GET /unified/stats
# Get database statistics
# Returns: Count of records in each table/collection
```

## 🧪 Testing Strategy

### **Types of Tests**
1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test how components work together
3. **End-to-End Tests**: Test complete user workflows
4. **API Tests**: Test all endpoints work correctly

### **Running Tests**
```bash
# Backend tests
cd backend
pytest                    # Run all tests
pytest -v                # Verbose output
pytest --cov=src         # With coverage report

# Frontend tests
cd frontend
npm test                 # Run unit tests
npm run test:e2e        # Run end-to-end tests
```

## 🐳 Docker Explained

Docker packages our application with all its dependencies into "containers" - think of them as lightweight virtual machines.

### **Why Use Docker?**
- **Consistency**: Same environment everywhere (development, testing, production)
- **Isolation**: Each service runs independently
- **Scalability**: Easy to run multiple instances
- **Deployment**: Simple to deploy anywhere

### **Docker Compose**
```yaml
# docker-compose.yml - Defines all our services
services:
  frontend:     # Next.js application
    build: ./frontend
    ports: ["3000:3000"]
    
  backend:      # FastAPI application
    build: ./backend
    ports: ["8000:8000"]
    
  postgres:     # PostgreSQL database
    image: postgres:15
    
  mongodb:      # MongoDB database
    image: mongo:6.0
```

## 🔧 Development Workflow

### **Setting Up Development Environment**
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/skillstacker.git
cd skillstacker

# 2. Start with Docker (easiest)
docker-compose up -d

# 3. Or set up manually
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### **Making Changes**
1. **Create Feature Branch**: `git checkout -b feature/new-feature`
2. **Make Changes**: Edit code, add features
3. **Test Changes**: Run tests to ensure nothing breaks
4. **Commit Changes**: `git commit -m "Add new feature"`
5. **Push Changes**: `git push origin feature/new-feature`
6. **Create Pull Request**: Request code review

## 🚀 Deployment Options

### **Development Deployment**
- **Local**: Run on your computer for development
- **Docker**: Use containers for consistent environment

### **Production Deployment**
- **Frontend**: Deploy to Vercel, Netlify, or AWS
- **Backend**: Deploy to Railway, Heroku, or AWS
- **Databases**: Use managed services (AWS RDS, MongoDB Atlas)

### **Environment Variables**
```bash
# Development (.env)
DATABASE_URL=postgresql://localhost:5432/skillstacker
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=dev-secret-key

# Production (.env.production)
DATABASE_URL=postgresql://prod-server:5432/skillstacker
MONGO_URL=mongodb://prod-cluster:27017
SECRET_KEY=super-secure-production-key
```

## 🔍 Monitoring & Debugging

### **Logging**
```python
# How we track what's happening
import logging
logger = logging.getLogger(__name__)

# Different log levels
logger.debug("Detailed info for debugging")
logger.info("General information")
logger.warning("Something unexpected happened")
logger.error("An error occurred")
logger.critical("Serious error, app might crash")
```

### **Error Handling**
```python
# How we handle errors gracefully
try:
    # Try to do something
    result = risky_operation()
except SpecificError as e:
    # Handle specific error
    logger.error(f"Specific error: {e}")
    return {"error": "Something went wrong"}
except Exception as e:
    # Handle any other error
    logger.error(f"Unexpected error: {e}")
    return {"error": "Internal server error"}
```

## 📈 Performance Optimization

### **Database Optimization**
- **Indexing**: Speed up searches
- **Connection Pooling**: Reuse database connections
- **Query Optimization**: Write efficient database queries

### **Frontend Optimization**
- **Code Splitting**: Load only needed code
- **Image Optimization**: Compress and resize images
- **Caching**: Store frequently used data

### **Backend Optimization**
- **Async Operations**: Handle multiple requests simultaneously
- **Response Compression**: Reduce data transfer
- **Rate Limiting**: Prevent abuse

## 🤝 Contributing Guidelines

### **Code Style**
- **Python**: Follow PEP 8 standards
- **TypeScript**: Use ESLint and Prettier
- **Comments**: Explain complex logic
- **Type Hints**: Use type annotations

### **Git Workflow**
1. **Fork** the repository
2. **Create** feature branch
3. **Make** changes with good commit messages
4. **Test** your changes
5. **Submit** pull request

### **Pull Request Checklist**
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

## 🎓 Learning Resources

### **Technologies to Learn**
1. **Python**: Backend programming language
2. **JavaScript/TypeScript**: Frontend programming
3. **SQL**: Database queries
4. **HTTP/REST**: API communication
5. **Git**: Version control

### **Recommended Learning Path**
1. **Beginner**: Start with Python basics and HTML/CSS
2. **Intermediate**: Learn FastAPI and React
3. **Advanced**: Study database design and deployment
4. **Expert**: Explore microservices and scaling

### **Useful Links**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)
- [MongoDB University](https://university.mongodb.com/)
- [Docker Getting Started](https://docs.docker.com/get-started/)

## 🆘 Troubleshooting Common Issues

### **Database Connection Issues**
```bash
# Check if databases are running
docker ps                    # See running containers
docker-compose logs postgres # Check PostgreSQL logs
docker-compose logs mongodb  # Check MongoDB logs
```

### **Port Already in Use**
```bash
# Find what's using the port
lsof -i :3000               # Check port 3000
lsof -i :8000               # Check port 8000

# Kill the process
kill -9 <process_id>
```

### **Module Not Found Errors**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 🎯 Next Steps

### **For Beginners**
1. Set up the development environment
2. Run the application locally
3. Explore the code structure
4. Make small changes and see the effects
5. Read through the API documentation

### **For Intermediate Developers**
1. Add new features
2. Write tests for existing code
3. Improve error handling
4. Optimize database queries
5. Add monitoring and logging

### **For Advanced Developers**
1. Implement microservices architecture
2. Add caching layer (Redis)
3. Set up CI/CD pipeline
4. Implement advanced security features
5. Scale for high traffic

---

**Remember**: Programming is about solving problems step by step. Don't try to understand everything at once. Start with the basics and gradually build your knowledge!

**Happy Coding! 🚀**