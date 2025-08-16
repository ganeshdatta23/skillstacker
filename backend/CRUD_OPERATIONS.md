# 🔧 CRUD Operations - Unified Data API

This document describes the comprehensive CRUD (Create, Read, Update, Delete) operations available in the SkillStacker unified data API.

## 🌐 Base URL
```
http://localhost:8000/unified
```

## 📋 Available Operations

### 🎬 Films (PostgreSQL)

#### Create Film
```http
POST /unified/films
```
**Parameters:**
- `title` (required): Film title
- `description` (optional): Film description
- `release_year` (optional): Release year
- `rental_rate` (optional): Rental rate (default: 4.99)
- `length` (optional): Film length in minutes
- `rating` (optional): Film rating (default: "G")

**Example:**
```bash
curl -X POST "http://localhost:8000/unified/films" \
  -d "title=My New Movie&description=A great film&release_year=2024&rating=PG-13"
```

#### Get Film
```http
GET /unified/films/{film_id}
```

#### Update Film
```http
PUT /unified/films/{film_id}
```
**Parameters:** Same as create (all optional)

#### Delete Film
```http
DELETE /unified/films/{film_id}
```

### 🎭 Actors (PostgreSQL)

#### Create Actor
```http
POST /unified/actors
```
**Parameters:**
- `first_name` (required): Actor's first name
- `last_name` (required): Actor's last name

#### Get Actor
```http
GET /unified/actors/{actor_id}
```

#### Update Actor
```http
PUT /unified/actors/{actor_id}
```

#### Delete Actor
```http
DELETE /unified/actors/{actor_id}
```

### ⭐ Reviews (MongoDB)

#### Create Review
```http
POST /unified/reviews
```
**Parameters:**
- `title` (required): Review title
- `content` (required): Review content
- `rating` (required): Rating 1-5
- `product_id` (optional): Associated product ID
- `user_id` (optional): User ID

#### Get Review
```http
GET /unified/reviews/{review_id}
```

#### Update Review
```http
PUT /unified/reviews/{review_id}
```

#### Delete Review
```http
DELETE /unified/reviews/{review_id}
```

### 📦 Bulk Operations

#### Bulk Create Films
```http
POST /unified/bulk/films
```
**Body:** JSON array of film objects (max 10)
```json
[
  {
    "title": "Film 1",
    "description": "Description 1",
    "rating": "PG"
  },
  {
    "title": "Film 2",
    "description": "Description 2",
    "rating": "PG-13"
  }
]
```

#### Bulk Create Reviews
```http
POST /unified/bulk/reviews
```
**Body:** JSON array of review objects (max 20)
```json
[
  {
    "title": "Great Product",
    "content": "Love it!",
    "rating": 5
  },
  {
    "title": "Good Product",
    "content": "Pretty good",
    "rating": 4
  }
]
```

### 🔍 Search & Analytics

#### Unified Search
```http
GET /unified/search?q={query}&category={category}&limit={limit}&skip={skip}
```
**Parameters:**
- `q` (required): Search query
- `category` (optional): Filter by category (films, actors, users, publications, reviews)
- `limit` (optional): Results limit (1-200, default: 50)
- `skip` (optional): Results to skip (default: 0)

#### Statistics
```http
GET /unified/stats
```
Returns comprehensive statistics from all data sources.

#### Categories
```http
GET /unified/categories
```
Returns all available categories from all data sources.

## 🧪 Testing

### Run the Test Suite
```bash
cd backend
python test_crud_operations.py
```

### Manual Testing Examples

#### 1. Create and Test a Film
```bash
# Create
curl -X POST "http://localhost:8000/unified/films" \
  -d "title=Test Movie&description=A test film&rating=PG-13"

# Get (replace {id} with actual ID)
curl "http://localhost:8000/unified/films/{id}"

# Update
curl -X PUT "http://localhost:8000/unified/films/{id}" \
  -d "title=Updated Movie&rating=R"

# Delete
curl -X DELETE "http://localhost:8000/unified/films/{id}"
```

#### 2. Create and Test a Review
```bash
# Create
curl -X POST "http://localhost:8000/unified/reviews" \
  -d "title=Great Product&content=I love this product!&rating=5"

# Get (replace {id} with actual MongoDB ObjectId)
curl "http://localhost:8000/unified/reviews/{id}"

# Update
curl -X PUT "http://localhost:8000/unified/reviews/{id}" \
  -d "title=Updated Review&rating=4"

# Delete
curl -X DELETE "http://localhost:8000/unified/reviews/{id}"
```

#### 3. Bulk Operations
```bash
# Bulk create films
curl -X POST "http://localhost:8000/unified/bulk/films" \
  -H "Content-Type: application/json" \
  -d '[
    {"title": "Bulk Film 1", "rating": "G"},
    {"title": "Bulk Film 2", "rating": "PG"}
  ]'

# Bulk create reviews
curl -X POST "http://localhost:8000/unified/bulk/reviews" \
  -H "Content-Type: application/json" \
  -d '[
    {"title": "Review 1", "content": "Great!", "rating": 5},
    {"title": "Review 2", "content": "Good", "rating": 4}
  ]'
```

#### 4. Search Operations
```bash
# Search all
curl "http://localhost:8000/unified/search?q=test"

# Search films only
curl "http://localhost:8000/unified/search?q=movie&category=films"

# Get statistics
curl "http://localhost:8000/unified/stats"

# Get categories
curl "http://localhost:8000/unified/categories"
```

## 🔒 Security Features

- **Input Sanitization**: All search terms are sanitized to prevent injection attacks
- **Parameter Validation**: Pydantic validation for all inputs
- **Rate Limiting Ready**: Endpoints are prepared for rate limiting implementation
- **Error Handling**: Comprehensive error handling with proper HTTP status codes

## 📊 Response Formats

### Success Response
```json
{
  "id": "123",
  "message": "Operation completed successfully",
  "data": { ... }
}
```

### Error Response
```json
{
  "detail": "Error description"
}
```

### Search Response
```json
{
  "query": "search term",
  "total_results": 25,
  "films": [...],
  "actors": [...],
  "users": [...],
  "publications": [...],
  "reviews": [...]
}
```

## 🚀 Performance Considerations

- **Database Indexing**: Proper indexes on searchable fields
- **Connection Pooling**: SQLAlchemy connection pooling for PostgreSQL
- **Async Operations**: MongoDB operations use async patterns where possible
- **Bulk Limits**: Bulk operations are limited to prevent resource exhaustion
- **Pagination**: Search results support pagination with skip/limit

## 🛠 Development Notes

### Adding New CRUD Operations
1. Define the model in `src/db/models.py` (PostgreSQL) or `src/db/mongo_models.py` (MongoDB)
2. Add the CRUD endpoints to `src/api/unified_data.py`
3. Update the test suite in `test_crud_operations.py`
4. Update this documentation

### Database Connections
- **PostgreSQL**: Uses SQLAlchemy ORM with connection pooling
- **MongoDB**: Uses PyMongo with connection validation
- **Error Handling**: Graceful degradation when databases are unavailable

### Testing Strategy
- **Unit Tests**: Individual CRUD operations
- **Integration Tests**: Cross-database operations
- **Performance Tests**: Bulk operations and search performance
- **Error Tests**: Database unavailability scenarios

## 📈 Monitoring & Logging

All operations are logged with appropriate levels:
- **INFO**: Successful operations
- **ERROR**: Failed operations with details
- **DEBUG**: Detailed operation traces (development only)

## 🔧 Configuration

Environment variables for database connections:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/skillstacker
MONGO_URL=mongodb://localhost:27017
```

## 🤝 Contributing

When adding new CRUD operations:
1. Follow the existing patterns
2. Add comprehensive error handling
3. Include input validation
4. Update tests and documentation
5. Consider security implications

---

**Built with ❤️ for the SkillStacker platform**