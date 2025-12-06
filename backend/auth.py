import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config
from models import db, Usuario

def generate_token(usuario_id):
    """Generar token JWT"""
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

def verify_token(token):
    """Verificar token JWT"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload['usuario_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token del header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'detail': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'detail': 'Token requerido'}), 401
        
        # Verificar token
        usuario_id = verify_token(token)
        if not usuario_id:
            return jsonify({'detail': 'Token inválido o expirado'}), 401
        
        # Obtener usuario
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'detail': 'Usuario no encontrado'}), 401
        
        return f(usuario, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorador para rutas que requieren rol de administrador"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Primero verificar autenticación
        @token_required
        def wrapper(usuario, *args, **kwargs):
            if usuario.rol != 'admin':
                return jsonify({'detail': 'Acceso denegado. Se requiere rol de administrador'}), 403
            return f(usuario, *args, **kwargs)
        
        return wrapper(*args, **kwargs)
    
    return decorated
