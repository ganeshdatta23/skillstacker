from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from api.auth import router as auth_router
from api.users import router as users_router
from api.products import router as products_router
from api.orders import router as orders_router
from api.films import router as films_router
from api.actors import router as actors_router
from api.categories import router as categories_router
# from api.publications import router as publications_router  # Temporarily disabled due to motor issues
from api.reviews import router as reviews_router
from api.unified_data import router as unified_router
from db.postgres import engine
from db.models import Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillStacker API",
    version="1.0.0",
    description="Enterprise Full-Stack Platform API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SkillStacker API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Routes
# app.include_router(overview_router, prefix="/api/v1/overview", tags=["Overview"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(films_router, prefix="/api/v1/films", tags=["Films"])
app.include_router(actors_router, prefix="/api/v1/actors", tags=["Actors"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["Categories"])
# app.include_router(publications_router, prefix="/api/v1/publications", tags=["Publications"])  # Temporarily disabled
app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(unified_router, prefix="/unified", tags=["Unified Data & CRUD"])