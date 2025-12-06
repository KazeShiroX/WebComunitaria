from flask import Blueprint, request, jsonify
from models import db, Noticia
from auth import token_required, admin_required
from sqlalchemy import or_

noticias_bp = Blueprint('noticias', __name__)

@noticias_bp.route('', methods=['GET'])
def get_noticias():
    """Obtener noticias con paginación y filtros"""
    # Parámetros de query
    pagina = request.args.get('pagina', 1, type=int)
    items_por_pagina = request.args.get('items_por_pagina', 4, type=int)
    categoria = request.args.get('categoria', None)
    busqueda = request.args.get('busqueda', None)
    
    # Query base
    query = Noticia.query
    
    # Filtro por categoría
    if categoria and categoria != 'Todos':
        query = query.filter_by(categoria=categoria)
    
    # Filtro de búsqueda
    if busqueda:
        search_term = f'%{busqueda}%'
        query = query.filter(
            or_(
                Noticia.titulo.like(search_term),
                Noticia.descripcion.like(search_term),
                Noticia.contenido.like(search_term)
            )
        )
    
    # Ordenar por fecha descendente
    query = query.order_by(Noticia.fecha.desc())
    
    # Paginación
    paginacion = query.paginate(page=pagina, per_page=items_por_pagina, error_out=False)
    
    return jsonify({
        'items': [noticia.to_dict() for noticia in paginacion.items],
        'total_items': paginacion.total,
        'total_paginas': paginacion.pages,
        'pagina_actual': paginacion.page,
        'items_por_pagina': items_por_pagina
    }), 200


@noticias_bp.route('/<int:id>', methods=['GET'])
def get_noticia(id):
    """Obtener una noticia por ID"""
    noticia = Noticia.query.get_or_404(id)
    return jsonify(noticia.to_dict()), 200


@noticias_bp.route('', methods=['POST'])
@token_required
def create_noticia(usuario):
    """Crear una nueva noticia (requiere autenticación)"""
    data = request.get_json()
    
    if not data or not data.get('titulo') or not data.get('descripcion'):
        return jsonify({'detail': 'Título y descripción requeridos'}), 400
    
    nueva_noticia = Noticia(
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        contenido=data.get('contenido', data['descripcion']),
        categoria=data['categoria'],
        imagen=data.get('imagen'),
        autor_id=usuario.id
    )
    
    db.session.add(nueva_noticia)
    db.session.commit()
    
    return jsonify(nueva_noticia.to_dict()), 201


@noticias_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_noticia(usuario, id):
    """Actualizar una noticia (requiere autenticación)"""
    noticia = Noticia.query.get_or_404(id)
    
    # Verificar que el usuario sea el autor o admin
    if noticia.autor_id != usuario.id and usuario.rol != 'admin':
        return jsonify({'detail': 'No tienes permiso para editar esta noticia'}), 403
    
    data = request.get_json()
    
    if 'titulo' in data:
        noticia.titulo = data['titulo']
    if 'descripcion' in data:
        noticia.descripcion = data['descripcion']
    if 'contenido' in data:
        noticia.contenido = data['contenido']
    if 'categoria' in data:
        noticia.categoria = data['categoria']
    if 'imagen' in data:
        noticia.imagen = data['imagen']
    
    db.session.commit()
    
    return jsonify(noticia.to_dict()), 200


@noticias_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_noticia(usuario, id):
    """Eliminar una noticia (requiere autenticación)"""
    noticia = Noticia.query.get_or_404(id)
    
    # Verificar que el usuario sea el autor o admin
    if noticia.autor_id != usuario.id and usuario.rol != 'admin':
        return jsonify({'detail': 'No tienes permiso para eliminar esta noticia'}), 403
    
    db.session.delete(noticia)
    db.session.commit()
    
    return jsonify({'message': 'Noticia eliminada correctamente'}), 200
