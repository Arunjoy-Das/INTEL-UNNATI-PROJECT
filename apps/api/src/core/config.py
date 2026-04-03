import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FactGuard"
    API_V1_STR: str = "/api/v1"
    
    # DB — fix Render's postgres:// → postgresql:// and fallback to SQLite
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    # REDIS (optional — not required for core functionality)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    class Config:
        case_sensitive = True

    def get_safe_database_url(self) -> str:
        """Fix Render's postgres:// scheme to postgresql:// for SQLAlchemy."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

settings = Settings()
