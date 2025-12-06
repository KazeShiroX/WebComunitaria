from flask import Blueprint, request, jsonify
from models import db, Usuario
from auth import generate_token, token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'detail': 'Email y contraseña requeridos'}), 400
    
    # Buscar usuario
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if not usuario or not usuario.check_password(data['password']):
        return jsonify({'detail': 'Credenciales incorrectas'}), 401
    
    # Generar token
    token = generate_token(usuario.id)
    
    return jsonify({
        'usuario': usuario.to_dict(),
        'access_token': token,
        'token_type': 'Bearer'
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint de registro"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('nombre'):
        return jsonify({'detail': 'Nombre, email y contraseña requeridos'}), 400
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'detail': 'El email ya está registrado'}), 400
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        rol='admin'  # Por defecto, todos los registros son admin para esta app simple
    )
    nuevo_usuario.set_password(data['password'])
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    # Generar token
    token = generate_token(nuevo_usuario.id)
    
    return jsonify({
        'usuario': nuevo_usuario.to_dict(),
        'access_token': token,
        'token_type': 'Bearer'
    }), 201


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(usuario):
    """Obtener información del usuario actual"""
    return jsonify(usuario.to_dict()), 200
