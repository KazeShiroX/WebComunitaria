from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
class RolEnum(str, Enum):
    admin = "admin"
    usuario = "usuario"

# Usuario Schemas
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    rol: RolEnum
    avatar: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class UsuarioConToken(BaseModel):
    usuario: UsuarioResponse
    access_token: str
    token_type: str = "bearer"

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

# Noticia Schemas
class NoticiaBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: str = Field(..., min_length=10)
    contenido: str = Field(..., min_length=10)
    categoria: str = Field(..., min_length=3, max_length=50)
    imagen: Optional[str] = None

class NoticiaCreate(NoticiaBase):
    pass

class NoticiaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    descripcion: Optional[str] = Field(None, min_length=10)
    contenido: Optional[str] = Field(None, min_length=10)
    categoria: Optional[str] = Field(None, min_length=3, max_length=50)
    imagen: Optional[str] = None

class NoticiaResponse(NoticiaBase):
    id: int
    fecha: datetime
    autor_id: int
    autor_nombre: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaginacionResponse(BaseModel):
    items: List[NoticiaResponse]
    total_items: int
    total_paginas: int
    pagina_actual: int
    items_por_pagina: int

# Respuestas generales
class MensajeResponse(BaseModel):
    message: str
    success: bool = True
