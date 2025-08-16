# 📚 SkillStacker API Documentation - Complete Guide

Welcome to the comprehensive API documentation for SkillStacker! This guide explains every endpoint in detail with examples that beginners can understand.

## 🎯 What is an API?

An **API (Application Programming Interface)** is like a waiter in a restaurant:
- You (the frontend) tell the waiter (API) what you want
- The waiter goes to the kitchen (backend/database) to get it
- The waiter brings back your order (data) in a nice format

## 🌐 Base URLs

| Environment | URL | When to Use |
|-------------|-----|-------------|
| **Development** | `http://localhost:8000` | When running locally |
| **Production** | `https://your-domain.com` | When deployed online |

## 🔑 Authentication

Most endpoints require authentication. Here's how it works:

### 1. Register a New User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "customer_id": 123,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "activebool": true,
    "is_admin": false
  }
}
```

### 2. Login Existing User
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure123"
}
```

### 3. Using the Token
Include the token in all future requests:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 🎬 Films API (PostgreSQL)

Films are movies stored in our PostgreSQL database with structured data.

### Create a New Film
```http
POST /unified/films
Content-Type: application/x-www-form-urlencoded

title=Inception&description=A mind-bending thriller&release_year=2010&rental_rate=5.99&length=148&rating=PG-13
```

**What each field means:**
- `title`: Movie name (required)
- `description`: Plot summary (optional)
- `release_year`: Year it was made (optional)
- `rental_rate`: Cost to rent in dollars (optional, default: 4.99)
- `length`: Duration in minutes (optional)
- `rating`: Age rating like G, PG, PG-13, R (optional, default: G)

**Response:**
```json
{
  "id": 1001,
  "title": "Inception",
  "message": "Film created successfully"
}
```

### Get a Specific Film
```http
GET /unified/films/1001
```

**Response:**
```json
{
  "id": 1001,
  "title": "Inception",
  "description": "A mind-bending thriller",
  "release_year": 2010,
  "rental_rate": "5.99",
  "length": 148,
  "rating": "PG-13"
}
```

### Update a Film
```http
PUT /unified/films/1001
Content-Type: application/x-www-form-urlencoded

title=Inception Updated&rating=R
```

**Note:** You only need to include fields you want to change!

### Delete a Film
```http
DELETE /unified/films/1001
```

**⚠️ Warning:** This permanently deletes the film!

## 🎭 Actors API (PostgreSQL)

Actors are people who appear in films.

### Create a New Actor
```http
POST /unified/actors
Content-Type: application/x-www-form-urlencoded

first_name=Leonardo&last_name=DiCaprio
```

### Get a Specific Actor
```http
GET /unified/actors/201
```

**Response:**
```json
{
  "id": 201,
  "first_name": "Leonardo",
  "last_name": "DiCaprio",
  "full_name": "Leonardo DiCaprio"
}
```

### Update an Actor
```http
PUT /unified/actors/201
Content-Type: application/x-www-form-urlencoded

first_name=Leo
```

### Delete an Actor
```http
DELETE /unified/actors/201
```

## ⭐ Reviews API (MongoDB)

Reviews are user opinions stored in MongoDB for flexibility.

### Create a New Review
```http
POST /unified/reviews
Content-Type: application/x-www-form-urlencoded

title=Amazing Movie!&content=I absolutely loved this film. The plot was incredible and the acting was superb.&rating=5&product_id=1001&user_id=123
```

**What each field means:**
- `title`: Review headline (required)
- `content`: Full review text (required)
- `rating`: 1-5 stars (required, must be between 1 and 5)
- `product_id`: Which film this reviews (optional)
- `user_id`: Who wrote the review (optional)

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Amazing Movie!",
  "rating": 5,
  "message": "Review created successfully"
}
```

### Get a Specific Review
```http
GET /unified/reviews/507f1f77bcf86cd799439011
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Amazing Movie!",
  "content": "I absolutely loved this film...",
  "rating": 5,
  "product_id": 1001,
  "user_id": 123,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update a Review
```http
PUT /unified/reviews/507f1f77bcf86cd799439011
Content-Type: application/x-www-form-urlencoded

title=Updated Review&rating=4
```

### Delete a Review
```http
DELETE /unified/reviews/507f1f77bcf86cd799439011
```

## 🔍 Search API

Search across all databases at once!

### Basic Search
```http
GET /unified/search?q=action
```

**Response:**
```json
{
  "query": "action",
  "total_results": 25,
  "films": [
    {
      "id": 1,
      "title": "Action Movie",
      "description": "An exciting action film",
      "rating": "PG-13",
      "length": 120,
      "type": "film"
    }
  ],
  "actors": [
    {
      "id": 1,
      "name": "Action Hero",
      "first_name": "Action",
      "last_name": "Hero",
      "type": "actor"
    }
  ],
  "users": [],
  "publications": [],
  "reviews": [
    {
      "id": "507f1f77bcf86cd799439012",
      "title": "Great action scenes",
      "content": "The action in this movie was incredible...",
      "rating": 5,
      "type": "review"
    }
  ]
}
```

### Search with Filters
```http
GET /unified/search?q=comedy&category=films&limit=10&skip=0
```

**Parameters:**
- `q`: What to search for (required)
- `category`: Limit to specific type (optional)
  - `films`: Only search movies
  - `actors`: Only search actors
  - `users`: Only search users
  - `publications`: Only search articles
  - `reviews`: Only search reviews
- `limit`: How many results (1-200, default: 50)
- `skip`: How many to skip for pagination (default: 0)

## 📦 Bulk Operations

Create multiple records at once for efficiency.

### Bulk Create Films
```http
POST /unified/bulk/films
Content-Type: application/json

[
  {
    "title": "Film 1",
    "description": "First film",
    "rating": "G"
  },
  {
    "title": "Film 2",
    "description": "Second film",
    "rating": "PG"
  }
]
```

**Response:**
```json
{
  "message": "Created 2 films successfully",
  "count": 2
}
```

### Bulk Create Reviews
```http
POST /unified/bulk/reviews
Content-Type: application/json

[
  {
    "title": "Great Movie",
    "content": "I loved it!",
    "rating": 5
  },
  {
    "title": "Good Film",
    "content": "Pretty good",
    "rating": 4
  }
]
```

## 📊 Statistics & Analytics

### Get Database Statistics
```http
GET /unified/stats
```

**Response:**
```json
{
  "postgresql": {
    "films": 1000,
    "actors": 603,
    "categories": 16,
    "users": 599,
    "rentals": 16044,
    "payments": 14596
  },
  "mongodb": {
    "publications": 50,
    "reviews": 25
  },
  "total": 2333
}
```

### Get All Categories
```http
GET /unified/categories
```

**Response:**
```json
{
  "film_ratings": ["G", "PG", "PG-13", "R", "NC-17"],
  "film_categories": ["Action", "Comedy", "Drama", "Horror"],
  "publication_types": ["blog", "article", "news"],
  "publication_groups": ["tech", "programming", "web-development"]
}
```

## 🚨 Error Handling

### Common HTTP Status Codes

| Code | Meaning | When It Happens |
|------|---------|-----------------|
| **200** | Success | Request worked perfectly |
| **201** | Created | New resource was created |
| **400** | Bad Request | Invalid input data |
| **401** | Unauthorized | Need to login first |
| **404** | Not Found | Resource doesn't exist |
| **422** | Validation Error | Data format is wrong |
| **500** | Server Error | Something went wrong on our end |

### Error Response Format
```json
{
  "detail": "Film not found"
}
```

### Common Errors and Solutions

#### 1. "Film not found" (404)
**Problem:** Trying to access a film that doesn't exist
**Solution:** Check the film ID is correct

#### 2. "Invalid search term" (400)
**Problem:** Search term contains invalid characters
**Solution:** Use only letters, numbers, spaces, and hyphens

#### 3. "MongoDB unavailable" (503)
**Problem:** MongoDB database is not running
**Solution:** Start MongoDB with `docker-compose up -d`

#### 4. "Validation error" (422)
**Problem:** Data doesn't match expected format
**Solution:** Check required fields and data types

## 🧪 Testing Examples

### Using cURL (Command Line)

#### Create a Film
```bash
curl -X POST "http://localhost:8000/unified/films" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Test Movie&description=A test film&rating=PG-13"
```

#### Search for Films
```bash
curl "http://localhost:8000/unified/search?q=test&category=films"
```

#### Get Statistics
```bash
curl "http://localhost:8000/unified/stats"
```

### Using JavaScript (Frontend)

#### Create a Film
```javascript
const response = await fetch('http://localhost:8000/unified/films', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'title=Test Movie&description=A test film&rating=PG-13'
});

const result = await response.json();
console.log(result);
```

#### Search
```javascript
const response = await fetch('http://localhost:8000/unified/search?q=action');
const results = await response.json();
console.log(results);
```

### Using Python (Backend/Scripts)

#### Create a Film
```python
import requests

response = requests.post(
    'http://localhost:8000/unified/films',
    data={
        'title': 'Test Movie',
        'description': 'A test film',
        'rating': 'PG-13'
    }
)

print(response.json())
```

#### Search
```python
import requests

response = requests.get(
    'http://localhost:8000/unified/search',
    params={'q': 'action', 'category': 'films'}
)

print(response.json())
```

## 🔧 Advanced Usage

### Pagination
When dealing with lots of data, use pagination:

```http
# Get first 10 results
GET /unified/search?q=movie&limit=10&skip=0

# Get next 10 results
GET /unified/search?q=movie&limit=10&skip=10

# Get results 21-30
GET /unified/search?q=movie&limit=10&skip=20
```

### Filtering by Category
```http
# Only search films
GET /unified/search?q=action&category=films

# Only search actors
GET /unified/search?q=smith&category=actors

# Only search reviews
GET /unified/search?q=great&category=reviews
```

### Partial Updates
You can update just specific fields:

```http
# Only update the title
PUT /unified/films/123
Content-Type: application/x-www-form-urlencoded

title=New Title

# Only update the rating
PUT /unified/films/123
Content-Type: application/x-www-form-urlencoded

rating=R

# Update multiple fields
PUT /unified/films/123
Content-Type: application/x-www-form-urlencoded

title=New Title&rating=R&rental_rate=6.99
```

## 🎓 Learning Exercises

### Beginner Exercises
1. **Create your first film** using the POST endpoint
2. **Search for it** using the search endpoint
3. **Update the film** with new information
4. **Create a review** for your film

### Intermediate Exercises
1. **Create multiple films** using bulk operations
2. **Implement pagination** in your searches
3. **Handle errors** gracefully in your code
4. **Create relationships** between films and actors

### Advanced Exercises
1. **Build a frontend** that uses these APIs
2. **Implement caching** for frequently accessed data
3. **Add authentication** to your requests
4. **Monitor performance** of your API calls

## 🔗 Related Documentation

- **[Complete Beginner's Guide](./COMPLETE_PROJECT_GUIDE.md)**: Understand the entire project
- **[CRUD Operations Guide](./backend/CRUD_OPERATIONS.md)**: Detailed CRUD examples
- **[Interactive API Docs](http://localhost:8000/docs)**: Test APIs in your browser
- **[Source Code](./backend/src/api/unified_data.py)**: See how it's implemented

## 💡 Tips for Success

### For Beginners
1. **Start with GET requests** - they're safe and don't change data
2. **Use the interactive docs** at http://localhost:8000/docs
3. **Test one endpoint at a time** before combining them
4. **Read error messages carefully** - they usually tell you what's wrong

### For Developers
1. **Always handle errors** in your code
2. **Use appropriate HTTP methods** (GET for reading, POST for creating, etc.)
3. **Validate input data** before sending requests
4. **Implement retry logic** for network failures
5. **Cache frequently accessed data** for better performance

### Best Practices
1. **Use HTTPS in production** for security
2. **Include authentication tokens** for protected endpoints
3. **Implement rate limiting** to prevent abuse
4. **Log API calls** for debugging and monitoring
5. **Version your APIs** for backward compatibility

---

**Happy API exploring! 🚀**

Remember: The best way to learn APIs is to use them. Start with simple GET requests and gradually work your way up to more complex operations!