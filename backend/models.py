from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class RolEnum(str, enum.Enum):
    admin = "admin"
    usuario = "usuario"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.usuario)
    avatar = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    noticias = relationship("Noticia", back_populates="autor")

class Noticia(Base):
    __tablename__ = "noticias"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    contenido = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False)
    imagen = Column(String(500), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    autor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    autor = relationship("Usuario", back_populates="noticias")
