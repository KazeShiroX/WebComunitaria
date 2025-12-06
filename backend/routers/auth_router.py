from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from database import get_db
from models import Usuario, RolEnum
from schemas import (
    UsuarioCreate, 
    UsuarioResponse, 
    UsuarioLogin, 
    UsuarioConToken,
    Token,
    MensajeResponse
)
from auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    get_current_user
)
from config import settings

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioConToken)
async def register(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """Registrar un nuevo usuario administrador"""
    # Verificar si el email ya existe
    result = await db.execute(select(Usuario).where(Usuario.email == usuario.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear usuario
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=get_password_hash(usuario.password),
        rol=RolEnum.admin,  # Todos los registros son admin por ahora
        avatar="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face"
    )
    
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    
    # Crear token
    access_token = create_access_token(
        data={"sub": nuevo_usuario.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return UsuarioConToken(
        usuario=UsuarioResponse.model_validate(nuevo_usuario),
        access_token=access_token
    )

@router.post("/login", response_model=UsuarioConToken)
async def login(form_data: UsuarioLogin, db: AsyncSession = Depends(get_db)):
    """Iniciar sesión"""
    result = await db.execute(select(Usuario).where(Usuario.email == form_data.email))
    usuario = result.scalar_one_or_none()
    
    if not usuario or not verify_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": usuario.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return UsuarioConToken(
        usuario=UsuarioResponse.model_validate(usuario),
        access_token=access_token
    )

@router.post("/login/form", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """Login con formulario OAuth2 (para Swagger UI)"""
    result = await db.execute(select(Usuario).where(Usuario.email == form_data.username))
    usuario = result.scalar_one_or_none()
    
    if not usuario or not verify_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": usuario.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(access_token=access_token)

@router.get("/me", response_model=UsuarioResponse)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return UsuarioResponse.model_validate(current_user)

@router.post("/logout", response_model=MensajeResponse)
async def logout(current_user: Usuario = Depends(get_current_user)):
    """Cerrar sesión (el token debe invalidarse en el cliente)"""
    return MensajeResponse(message="Sesión cerrada correctamente")
