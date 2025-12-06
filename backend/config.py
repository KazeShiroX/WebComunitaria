import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base de datos
    # Railway provides DATABASE_URL, otherwise use individual vars
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL and DATABASE_URL.startswith('mysql://'):
        # Railway MySQL format
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('mysql://', 'mysql+pymysql://')
    else:
        # Local development
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'Ruben2004')
        DB_NAME = os.getenv('DB_NAME', 'webcomunitaria')
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # CORS - Allow Railway domain
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200').split(',')
    
    # Port for Railway
    PORT = int(os.getenv('PORT', 8000))
