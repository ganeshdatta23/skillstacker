from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from api.auth import router as auth_router
from api.users import router as users_router
from api.products import router as products_router
from api.orders import router as orders_router
from api.reviews import router as reviews_router
from core.config import settings
# from db.mongo import connect_to_mongo, close_mongo_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log") if settings.environment == "production" else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting SkillStacker API...")
    logger.info("✅ API started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down SkillStacker API...")
    logger.info("✅ API shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="SkillStacker API",
    version="1.0.0",
    description="""
    🚀 **SkillStacker** - Enterprise Full-Stack Platform API
    
    A world-class REST API built with FastAPI, featuring:
    
    * **🔐 JWT Authentication** - Secure token-based authentication
    * **👥 User Management** - Registration, login, profile management
    * **📦 Product Catalog** - Advanced search and filtering
    * **⭐ Review System** - MongoDB-powered reviews and ratings
    * **📊 Analytics Ready** - Built for data insights
    
    ## Authentication
    
    Most endpoints require authentication. Include your JWT token in the Authorization header:
    ```
    Authorization: Bearer <your-jwt-token>
    ```
    
    ## Rate Limiting
    
    API calls are rate-limited to ensure fair usage and system stability.
    
    ## Support
    
    For support, email support@skillstacker.com or visit our documentation.
    """,
    contact={
        "name": "SkillStacker Team",
        "url": "https://skillstacker.com/contact",
        "email": "support@skillstacker.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

# Security Middleware
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["skillstacker.com", "*.skillstacker.com", "localhost"]
    )

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://skillstacker.vercel.app",
        "https://*.skillstacker.com"
    ] if settings.environment == "development" else [
        "https://skillstacker.com",
        "https://*.skillstacker.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    if settings.environment == "development":
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Internal server error: {str(exc)}",
                "type": type(exc).__name__
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with proper logging"""
    logger.warning(f"HTTP {exc.status_code} error occurred")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Health Check Endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns the current status of the API and its dependencies.
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "🚀 Welcome to SkillStacker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "environment": settings.environment
    }

# API Routes
app.include_router(
    auth_router, 
    prefix=f"{settings.api_v1_prefix}/auth", 
    tags=["🔐 Authentication"]
)

app.include_router(
    users_router, 
    prefix=f"{settings.api_v1_prefix}/users", 
    tags=["👥 Users"]
)

app.include_router(
    products_router, 
    prefix=f"{settings.api_v1_prefix}/products", 
    tags=["📦 Products"]
)

app.include_router(
    orders_router, 
    prefix=f"{settings.api_v1_prefix}/orders", 
    tags=["🛒 Orders"]
)

app.include_router(
    reviews_router, 
    prefix=f"{settings.api_v1_prefix}/reviews", 
    tags=["⭐ Reviews"]
)

# Startup message
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting SkillStacker API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
        log_level="info"
    )