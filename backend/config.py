import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base de datos - soporta DATABASE_URL (Railway/DOM Cloud) y fallback a MySQL local
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # Railway MySQL/PostgreSQL format
        if DATABASE_URL.startswith('mysql://'):
            SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('mysql://', 'mysql+pymysql://')
        elif DATABASE_URL.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
        else:
            # SQLite u otros (DOM Cloud usa sqlite)
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local development
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_NAME = os.getenv('DB_NAME', 'webcomunitaria')
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
<<<<<<< Updated upstream
    # CORS
    CORS_ORIGINS = ["*"]
=======
    # CORS - soporta CORS_ORIGINS como variable de entorno (separadas por coma)
    _extra_origins = [o.strip() for o in os.getenv('CORS_ORIGINS', '').split(',') if o.strip()]
    CORS_ORIGINS = [
        'http://localhost:4200',
        'http://127.0.0.1:4200',
        os.getenv('RAILWAY_PUBLIC_DOMAIN', ''),
        f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN', '')}"
    ] + _extra_origins
>>>>>>> Stashed changes
    
    # Puerto
    PORT = int(os.getenv('PORT', 8000))
    
    # Debug
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
