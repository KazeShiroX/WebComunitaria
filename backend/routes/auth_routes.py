from flask import Blueprint, request, jsonify
from models import db, Usuario, Notificacion
from auth import generate_token, token_required

auth_bp = Blueprint('auth', __name__)


# ─── AUTH ────────────────────────────────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'detail': 'Email y contraseña requeridos'}), 400

    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not usuario.check_password(data['password']):
        return jsonify({'detail': 'Credenciales incorrectas'}), 401

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

    existing = Usuario.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'detail': 'El email ya está registrado'}), 400

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        rol='usuario'
    )
    nuevo_usuario.set_password(data['password'])

    db.session.add(nuevo_usuario)
    db.session.commit()

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


@auth_bp.route('/me', methods=['PUT'])
@token_required
def update_profile(usuario):
    """Actualizar perfil del usuario autenticado"""
    data = request.get_json()

    if not data:
        return jsonify({'detail': 'Sin datos'}), 400

    if 'nombre' in data and data['nombre'].strip():
        usuario.nombre = data['nombre'].strip()

    if 'avatar' in data:
        usuario.avatar = data['avatar'] or None

    db.session.commit()

    return jsonify(usuario.to_dict()), 200


# ─── NOTIFICACIONES ──────────────────────────────────────────────────────────

@auth_bp.route('/notificaciones', methods=['GET'])
@token_required
def get_notificaciones(usuario):
    """Obtener notificaciones del usuario autenticado"""
    limite = request.args.get('limite', 20, type=int)

    notifs = Notificacion.query.filter_by(usuario_id=usuario.id)\
        .order_by(Notificacion.fecha.desc())\
        .limit(limite).all()

    no_leidas = Notificacion.query.filter_by(
        usuario_id=usuario.id, leida=False
    ).count()

    return jsonify({
        'items': [n.to_dict() for n in notifs],
        'no_leidas': no_leidas
    }), 200


@auth_bp.route('/notificaciones/<int:notif_id>/leer', methods=['POST'])
@token_required
def marcar_leida(usuario, notif_id):
    """Marcar una notificación como leída"""
    notif = Notificacion.query.filter_by(
        id=notif_id, usuario_id=usuario.id
    ).first_or_404()

    notif.leida = True
    db.session.commit()
    return jsonify({'ok': True}), 200


@auth_bp.route('/notificaciones/leer-todas', methods=['POST'])
@token_required
def marcar_todas_leidas(usuario):
    """Marcar todas las notificaciones del usuario como leídas"""
    Notificacion.query.filter_by(
        usuario_id=usuario.id, leida=False
    ).update({'leida': True})
    db.session.commit()
    return jsonify({'ok': True}), 200


# ─── GESTIÓN DE USUARIOS (solo admin) ────────────────────────────────────────

@auth_bp.route('/usuarios', methods=['GET'])
@token_required
def get_usuarios(usuario):
    """Listar todos los usuarios (solo admin)"""
    if usuario.rol != 'admin':
        return jsonify({'detail': 'Acceso solo para admin'}), 403

    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return jsonify({
        'items': [u.to_dict() for u in usuarios]
    }), 200


@auth_bp.route('/usuarios/<int:usuario_id>/rol', methods=['PATCH'])
@token_required
def cambiar_rol(usuario, usuario_id):
    """Cambiar el rol de un usuario (solo admin, no puede cambiar su propio rol)"""
    if usuario.rol != 'admin':
        return jsonify({'detail': 'Acceso solo para admin'}), 403

    if usuario.id == usuario_id:
        return jsonify({'detail': 'No puedes cambiar tu propio rol'}), 400

    data = request.get_json()
    nuevo_rol = data.get('rol') if data else None

    if nuevo_rol not in ('admin', 'moderador', 'usuario'):
        return jsonify({'detail': 'Rol inválido. Válidos: admin, moderador, usuario'}), 400

    target = Usuario.query.get_or_404(usuario_id)

    if target.rol == 'admin':
        return jsonify({'detail': 'No se puede cambiar el rol de un administrador'}), 400

    target.rol = nuevo_rol
    db.session.commit()

    return jsonify(target.to_dict()), 200

