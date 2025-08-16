# SkillStacker Testing Guide

## Quick Test Commands

### 1. Full System Test
```bash
# Windows
test-suite.bat

# Linux/Mac  
chmod +x test-suite.sh && ./test-suite.sh
```

### 2. Backend Unit Tests
```bash
# Windows
run-backend-tests.bat

# Linux/Mac
cd backend && pytest tests/ -v
```

### 3. Manual API Testing
```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/v1/products/

# Login test
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@skillstacker.com&password=password123"
```

## Test Coverage

### Infrastructure Tests
- [x] Docker containers startup
- [x] Database connectivity
- [x] Service health checks
- [x] Port accessibility

### Backend API Tests  
- [x] Authentication endpoints
- [x] Product CRUD operations
- [x] Review system (MongoDB)
- [x] User management
- [x] Error handling
- [x] Input validation

### Frontend Tests
- [x] Page loading
- [x] User authentication flow
- [x] Product browsing
- [x] Dashboard functionality
- [x] Responsive design

### Integration Tests
- [x] Frontend-Backend communication
- [x] Database integration
- [x] Authentication flow
- [x] API error handling

### Security Tests
- [x] JWT token validation
- [x] Protected route access
- [x] Input sanitization
- [x] CORS configuration

## Performance Benchmarks

### Expected Response Times
- Health check: < 50ms
- Product listing: < 200ms
- User authentication: < 300ms
- Database queries: < 100ms

### Load Testing
```bash
# Install Apache Bench
# Test concurrent requests
ab -n 100 -c 10 http://localhost:8000/api/v1/products/
```

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database connection**: Ensure containers are running
3. **Authentication errors**: Check JWT secret configuration
4. **CORS issues**: Verify frontend URL in backend settings

### Debug Commands
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Check database data
docker-compose exec postgres psql -U postgres -d skillstacker -c "SELECT * FROM users LIMIT 5;"

# Test API directly
curl -v http://localhost:8000/api/v1/products/
```

## Test Results Format

### Success Criteria
All tests must return:
- HTTP 200 for successful operations
- HTTP 401 for unauthorized access
- HTTP 404 for missing resources
- HTTP 422 for validation errors

### Expected Data
- Users table: 2+ demo users
- Products table: 10+ sample products
- Reviews collection: Sample reviews in MongoDB
- Authentication: Valid JWT tokens

## Automated Testing

### CI/CD Pipeline
Tests run automatically on:
- Pull requests
- Main branch pushes
- Release tags

### Local Testing Workflow
1. Start services: `start-dev.bat`
2. Run tests: `test-suite.bat`
3. Check results: All tests should pass
4. Fix issues: Debug and retest
5. Deploy: Ready for production

## Performance Monitoring

### Key Metrics
- API response time < 200ms
- Database query time < 100ms
- Frontend load time < 2s
- Memory usage < 512MB per service

### Monitoring Commands
```bash
# Check resource usage
docker stats

# Monitor API performance
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/products/
```

This testing suite ensures production-ready quality and enterprise-grade reliability.