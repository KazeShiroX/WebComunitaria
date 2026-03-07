from flask import Blueprint, request, jsonify
from models import db, Comentario, Reaccion, Noticia
from auth import token_required

comentarios_bp = Blueprint('comentarios', __name__)


# ─── COMENTARIOS ─────────────────────────────────────────────────────────────

@comentarios_bp.route('/noticias/<int:noticia_id>/comentarios', methods=['GET'])
def get_comentarios(noticia_id):
    """Obtener comentarios de una noticia, paginados"""
    Noticia.query.get_or_404(noticia_id)

    pagina = request.args.get('pagina', 1, type=int)
    items_por_pagina = request.args.get('items_por_pagina', 5, type=int)

    paginacion = Comentario.query.filter_by(noticia_id=noticia_id)\
        .order_by(Comentario.fecha.asc())\
        .paginate(page=pagina, per_page=items_por_pagina, error_out=False)

    return jsonify({
        'items': [c.to_dict() for c in paginacion.items],
        'total': paginacion.total,
        'total_paginas': paginacion.pages,
        'pagina_actual': paginacion.page,
        'items_por_pagina': items_por_pagina
    }), 200


@comentarios_bp.route('/noticias/<int:noticia_id>/comentarios', methods=['POST'])
@token_required
def crear_comentario(usuario, noticia_id):
    """Crear un comentario (requiere autenticación)"""
    Noticia.query.get_or_404(noticia_id)

    data = request.get_json()

    if not data or not data.get('texto') or not data['texto'].strip():
        return jsonify({'detail': 'El texto del comentario no puede estar vacío'}), 400

    comentario = Comentario(
        noticia_id=noticia_id,
        usuario_id=usuario.id,
        texto=data['texto'].strip()
    )

    db.session.add(comentario)
    db.session.commit()

    return jsonify(comentario.to_dict()), 201


@comentarios_bp.route('/comentarios/<int:comentario_id>', methods=['DELETE'])
@token_required
def eliminar_comentario(usuario, comentario_id):
    """Eliminar un comentario — autor, moderador o admin"""
    comentario = Comentario.query.get_or_404(comentario_id)

    puede_eliminar = (
        comentario.usuario_id == usuario.id or
        usuario.rol in ('admin', 'moderador')
    )

    if not puede_eliminar:
        return jsonify({'detail': 'No tienes permiso para eliminar este comentario'}), 403

    db.session.delete(comentario)
    db.session.commit()

    return jsonify({'message': 'Comentario eliminado'}), 200


# ─── REACCIONES ──────────────────────────────────────────────────────────────

TIPOS_VALIDOS = {'like', 'love', 'wow', 'sad', 'angry'}


@comentarios_bp.route('/noticias/<int:noticia_id>/reacciones', methods=['GET'])
def get_reacciones(noticia_id):
    """Obtener conteo de reacciones de una noticia"""
    Noticia.query.get_or_404(noticia_id)

    reacciones = Reaccion.query.filter_by(noticia_id=noticia_id).all()

    conteo = {'like': 0, 'love': 0, 'wow': 0, 'sad': 0, 'angry': 0}
    for r in reacciones:
        conteo[r.tipo] += 1

    return jsonify({'conteo': conteo, 'total': len(reacciones)}), 200


@comentarios_bp.route('/noticias/<int:noticia_id>/reacciones/mi-reaccion', methods=['GET'])
@token_required
def get_mi_reaccion(usuario, noticia_id):
    """Obtener la reacción del usuario actual"""
    Noticia.query.get_or_404(noticia_id)

    reaccion = Reaccion.query.filter_by(
        noticia_id=noticia_id, usuario_id=usuario.id
    ).first()

    return jsonify({'tipo': reaccion.tipo if reaccion else None}), 200


@comentarios_bp.route('/noticias/<int:noticia_id>/reacciones', methods=['POST'])
@token_required
def reaccionar(usuario, noticia_id):
    """Agregar/cambiar reacción — toggle si mismo tipo"""
    Noticia.query.get_or_404(noticia_id)

    data = request.get_json()
    tipo = data.get('tipo') if data else None

    if not tipo or tipo not in TIPOS_VALIDOS:
        return jsonify({'detail': f'Tipo inválido. Válidos: {list(TIPOS_VALIDOS)}'}), 400

    existente = Reaccion.query.filter_by(
        noticia_id=noticia_id, usuario_id=usuario.id
    ).first()

    if existente:
        if existente.tipo == tipo:
            db.session.delete(existente)
            db.session.commit()
            return jsonify({'message': 'Reacción quitada', 'tipo': None}), 200
        else:
            existente.tipo = tipo
            db.session.commit()
            return jsonify(existente.to_dict()), 200
    else:
        reaccion = Reaccion(noticia_id=noticia_id, usuario_id=usuario.id, tipo=tipo)
        db.session.add(reaccion)
        db.session.commit()
        return jsonify(reaccion.to_dict()), 201


@comentarios_bp.route('/noticias/<int:noticia_id>/reacciones', methods=['DELETE'])
@token_required
def quitar_reaccion(usuario, noticia_id):
    """Quitar la reacción del usuario actual"""
    reaccion = Reaccion.query.filter_by(
        noticia_id=noticia_id, usuario_id=usuario.id
    ).first()

    if reaccion:
        db.session.delete(reaccion)
        db.session.commit()

    return jsonify({'message': 'Reacción eliminada'}), 200
