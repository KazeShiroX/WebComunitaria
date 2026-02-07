from flask import Blueprint, request, jsonify
from models import db, Usuario
from auth import generate_token, token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login"""
    data = request.get_json()
    
    print(f"DEBUG LOGIN Attempt: Data received: {data}")

    if not data or not data.get('email') or not data.get('password'):
        print("DEBUG LOGIN: Missing fields")
        return jsonify({'detail': 'Email y contraseña requeridos'}), 400
    
    # Buscar usuario
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if usuario:
        print(f"DEBUG LOGIN: User found: {usuario.email}, Role: {usuario.rol}")
        is_valid = usuario.check_password(data['password'])
        print(f"DEBUG LOGIN: Password valid? {is_valid}")
        if not is_valid:
            print(f"DEBUG LOGIN: Hash in DB: {usuario.password_hash}")
    else:
        print(f"DEBUG LOGIN: User NOT found for email: {data['email']}")

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
    
    print(f"DEBUG REGISTER Attempt: Data received: {data}")

    if not data or not data.get('email') or not data.get('password') or not data.get('nombre'):
        print("DEBUG REGISTER: Missing fields")
        return jsonify({'detail': 'Nombre, email y contraseña requeridos'}), 400
    
    # Verificar si el usuario ya existe
    existing = Usuario.query.filter_by(email=data['email']).first()
    if existing:
        print(f"DEBUG REGISTER: Email already exists: {data['email']}")
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
