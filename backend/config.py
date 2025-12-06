from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Ríos Informa API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./noticias.db"
    
    # JWT Settings
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:4200", "http://127.0.0.1:4200"]
    
    class Config:
        env_file = ".env"

settings = Settings()
