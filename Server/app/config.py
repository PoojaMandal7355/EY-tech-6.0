from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./pharmapilot.db"
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    API_V1_PREFIX: str = "/api/v1"
    # Comma-separated list of allowed origins. Added 5174 for Vite fallback port and 127.0.0.1 variants.
    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://localhost:5173,"
        "http://localhost:5174,"
        "http://127.0.0.1:5173,"
        "http://127.0.0.1:5174"
    )
    
    # Security settings - Simplified for development
    MAX_LOGIN_ATTEMPTS: int = 999  # Disable account lockout
    ACCOUNT_LOCKOUT_MINUTES: int = 0
    MIN_PASSWORD_LENGTH: int = 8  # Minimum 8 characters
    MAX_PASSWORD_LENGTH: int = 200  # Allow longer passwords
    REQUIRE_PASSWORD_UPPERCASE: bool = False  # Not required
    REQUIRE_PASSWORD_LOWERCASE: bool = False  # Not required
    REQUIRE_PASSWORD_DIGIT: bool = False  # Not required
    REQUIRE_PASSWORD_SPECIAL: bool = False  # Not required
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Gmail Configuration
    GMAIL_EMAIL: Optional[str] = None
    GMAIL_APP_PASSWORD: Optional[str] = None
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields from .env

settings = Settings()
