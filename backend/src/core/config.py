from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database URLs
    database_url: str = "sqlite:///./skillstacker.db"  # Use SQLite by default
    mongo_url: str = "mongodb://localhost:27017"
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production-12345678901234567890"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "SkillStacker API"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()