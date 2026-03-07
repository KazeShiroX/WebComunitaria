from flask import Blueprint, request, jsonify
from models import db, Evento, Usuario
from auth import token_required
from datetime import datetime

eventos_bp = Blueprint('eventos', __name__)

CATEGORIAS_VALIDAS = ['Cultural', 'Deportivo', 'Cívico', 'Comunitario', 'Educativo', 'General']


@eventos_bp.route('', methods=['GET'])
def get_eventos():
    """Listar eventos (con filtro de categoría opcional)"""
    cat = request.args.get('categoria', '')
    q = Evento.query
    if cat and cat != 'Todos':
        q = q.filter(Evento.categoria == cat)
    # Ordenar: próximos primero, luego pasados
    eventos = q.order_by(Evento.fecha_evento.asc()).all()
    return jsonify([e.to_dict() for e in eventos]), 200


@eventos_bp.route('/<int:id>', methods=['GET'])
def get_evento(id):
    evento = Evento.query.get_or_404(id)
    return jsonify(evento.to_dict()), 200


@eventos_bp.route('', methods=['POST'])
@token_required
def crear_evento(usuario):
    """Crear evento (admin o moderador)"""
    if usuario.rol not in ('admin', 'moderador'):
        return jsonify({'detail': 'Sin permiso para crear eventos'}), 403

    data = request.get_json()
    campos = ['titulo', 'descripcion', 'fecha_evento']
    for c in campos:
        if not data.get(c):
            return jsonify({'detail': f'Campo requerido: {c}'}), 400

    try:
        fecha = datetime.fromisoformat(data['fecha_evento'].replace('Z', '+00:00'))
    except Exception:
        return jsonify({'detail': 'Formato de fecha inválido (usa ISO 8601)'}), 400

    evento = Evento(
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        categoria=data.get('categoria', 'General'),
        fecha_evento=fecha,
        imagen=data.get('imagen', ''),
        lugar=data.get('lugar', ''),
        autor_id=usuario.id
    )
    db.session.add(evento)
    db.session.commit()
    return jsonify(evento.to_dict()), 201


@eventos_bp.route('/<int:id>', methods=['PUT'])
@token_required
def actualizar_evento(usuario, id):
    """Actualizar evento (admin o moderador, o autor)"""
    evento = Evento.query.get_or_404(id)
    if evento.autor_id != usuario.id and usuario.rol not in ('admin', 'moderador'):
        return jsonify({'detail': 'Sin permiso'}), 403

    data = request.get_json()
    if 'titulo' in data:        evento.titulo = data['titulo']
    if 'descripcion' in data:   evento.descripcion = data['descripcion']
    if 'categoria' in data:     evento.categoria = data['categoria']
    if 'imagen' in data:        evento.imagen = data['imagen']
    if 'lugar' in data:         evento.lugar = data['lugar']
    if 'fecha_evento' in data:
        try:
            evento.fecha_evento = datetime.fromisoformat(data['fecha_evento'].replace('Z', '+00:00'))
        except Exception:
            return jsonify({'detail': 'Formato de fecha inválido'}), 400

    db.session.commit()
    return jsonify(evento.to_dict()), 200


@eventos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def eliminar_evento(usuario, id):
    """Eliminar evento (admin o moderador, o autor)"""
    evento = Evento.query.get_or_404(id)
    if evento.autor_id != usuario.id and usuario.rol not in ('admin', 'moderador'):
        return jsonify({'detail': 'Sin permiso'}), 403

    db.session.delete(evento)
    db.session.commit()
    return jsonify({'detail': 'Evento eliminado'}), 200
