from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from math import ceil

from database import get_db
from models import Noticia, Usuario
from schemas import (
    NoticiaCreate,
    NoticiaUpdate,
    NoticiaResponse,
    PaginacionResponse,
    MensajeResponse
)
from auth import get_current_admin

router = APIRouter(prefix="/api/noticias", tags=["Noticias"])

@router.get("", response_model=PaginacionResponse)
async def listar_noticias(
    pagina: int = Query(1, ge=1, description="Número de página"),
    items_por_pagina: int = Query(4, ge=1, le=50, description="Items por página"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    busqueda: Optional[str] = Query(None, description="Buscar en título y descripción"),
    db: AsyncSession = Depends(get_db)
):
    """Listar noticias con paginación y filtros"""
    # Query base
    query = select(Noticia).order_by(desc(Noticia.fecha))
    count_query = select(func.count(Noticia.id))
    
    # Filtro por categoría
    if categoria and categoria != "Todos":
        query = query.where(Noticia.categoria == categoria)
        count_query = count_query.where(Noticia.categoria == categoria)
    
    # Búsqueda
    if busqueda:
        busqueda_pattern = f"%{busqueda}%"
        query = query.where(
            (Noticia.titulo.ilike(busqueda_pattern)) | 
            (Noticia.descripcion.ilike(busqueda_pattern))
        )
        count_query = count_query.where(
            (Noticia.titulo.ilike(busqueda_pattern)) | 
            (Noticia.descripcion.ilike(busqueda_pattern))
        )
    
    # Contar total
    total_result = await db.execute(count_query)
    total_items = total_result.scalar()
    
    # Paginación
    offset = (pagina - 1) * items_por_pagina
    query = query.offset(offset).limit(items_por_pagina)
    
    # Ejecutar query
    result = await db.execute(query)
    noticias = result.scalars().all()
    
    # Obtener nombres de autores
    items = []
    for noticia in noticias:
        autor_result = await db.execute(select(Usuario.nombre).where(Usuario.id == noticia.autor_id))
        autor_nombre = autor_result.scalar_one_or_none()
        
        noticia_dict = {
            "id": noticia.id,
            "titulo": noticia.titulo,
            "descripcion": noticia.descripcion,
            "contenido": noticia.contenido,
            "categoria": noticia.categoria,
            "imagen": noticia.imagen,
            "fecha": noticia.fecha,
            "autor_id": noticia.autor_id,
            "autor_nombre": autor_nombre,
            "created_at": noticia.created_at
        }
        items.append(NoticiaResponse(**noticia_dict))
    
    total_paginas = ceil(total_items / items_por_pagina) if total_items > 0 else 1
    
    return PaginacionResponse(
        items=items,
        total_items=total_items,
        total_paginas=total_paginas,
        pagina_actual=pagina,
        items_por_pagina=items_por_pagina
    )

@router.get("/categorias")
async def listar_categorias():
    """Listar todas las categorías disponibles"""
    return ["Todos", "Noticias Locales", "Deportes", "Cultura", "Comunidad"]

@router.get("/{noticia_id}", response_model=NoticiaResponse)
async def obtener_noticia(noticia_id: int, db: AsyncSession = Depends(get_db)):
    """Obtener una noticia por ID"""
    result = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()
    
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noticia no encontrada"
        )
    
    autor_result = await db.execute(select(Usuario.nombre).where(Usuario.id == noticia.autor_id))
    autor_nombre = autor_result.scalar_one_or_none()
    
    return NoticiaResponse(
        id=noticia.id,
        titulo=noticia.titulo,
        descripcion=noticia.descripcion,
        contenido=noticia.contenido,
        categoria=noticia.categoria,
        imagen=noticia.imagen,
        fecha=noticia.fecha,
        autor_id=noticia.autor_id,
        autor_nombre=autor_nombre,
        created_at=noticia.created_at
    )

@router.post("", response_model=NoticiaResponse, status_code=status.HTTP_201_CREATED)
async def crear_noticia(
    noticia: NoticiaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Crear una nueva noticia (requiere ser admin)"""
    nueva_noticia = Noticia(
        titulo=noticia.titulo,
        descripcion=noticia.descripcion,
        contenido=noticia.contenido,
        categoria=noticia.categoria,
        imagen=noticia.imagen or "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=250&fit=crop",
        autor_id=current_user.id
    )
    
    db.add(nueva_noticia)
    await db.commit()
    await db.refresh(nueva_noticia)
    
    return NoticiaResponse(
        id=nueva_noticia.id,
        titulo=nueva_noticia.titulo,
        descripcion=nueva_noticia.descripcion,
        contenido=nueva_noticia.contenido,
        categoria=nueva_noticia.categoria,
        imagen=nueva_noticia.imagen,
        fecha=nueva_noticia.fecha,
        autor_id=nueva_noticia.autor_id,
        autor_nombre=current_user.nombre,
        created_at=nueva_noticia.created_at
    )

@router.put("/{noticia_id}", response_model=NoticiaResponse)
async def actualizar_noticia(
    noticia_id: int,
    noticia_update: NoticiaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Actualizar una noticia (requiere ser admin)"""
    result = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()
    
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noticia no encontrada"
        )
    
    # Actualizar campos
    update_data = noticia_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(noticia, field, value)
    
    await db.commit()
    await db.refresh(noticia)
    
    autor_result = await db.execute(select(Usuario.nombre).where(Usuario.id == noticia.autor_id))
    autor_nombre = autor_result.scalar_one_or_none()
    
    return NoticiaResponse(
        id=noticia.id,
        titulo=noticia.titulo,
        descripcion=noticia.descripcion,
        contenido=noticia.contenido,
        categoria=noticia.categoria,
        imagen=noticia.imagen,
        fecha=noticia.fecha,
        autor_id=noticia.autor_id,
        autor_nombre=autor_nombre,
        created_at=noticia.created_at
    )

@router.delete("/{noticia_id}", response_model=MensajeResponse)
async def eliminar_noticia(
    noticia_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Eliminar una noticia (requiere ser admin)"""
    result = await db.execute(select(Noticia).where(Noticia.id == noticia_id))
    noticia = result.scalar_one_or_none()
    
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noticia no encontrada"
        )
    
    await db.delete(noticia)
    await db.commit()
    
    return MensajeResponse(message="Noticia eliminada correctamente")
