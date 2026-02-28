import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- BASE DE DATOS ---
    # Soporta DATABASE_URL (Railway/DOM Cloud) y fallback a MySQL local
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # Corrección de protocolos para SQLAlchemy
        if DATABASE_URL.startswith('mysql://'):
            SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)
        elif DATABASE_URL.startswith('postgres://'):
            # SQLAlchemy requiere 'postgresql://' en lugar de 'postgres://'
            SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Configuración para Desarrollo Local
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_NAME = os.getenv('DB_NAME', 'webcomunitaria')
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- SEGURIDAD (JWT) ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # --- CORS ---
    # Combina orígenes locales, de Railway y variables de entorno
    _extra_origins = [o.strip() for o in os.getenv('CORS_ORIGINS', '').split(',') if o.strip()]
    
    CORS_ORIGINS = [
        'http://localhost:4200',
        'http://127.0.0.1:4200',
    ] + _extra_origins

    # Agregar dominio de Railway si existe
    railway_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN')
    if railway_domain:
        CORS_ORIGINS.append(f"https://{railway_domain}")
    
    # --- SERVIDOR ---
    PORT = int(os.getenv('PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'