#!/usr/bin/env python3
"""
Script para inicializar el usuario administrador en la base de datos
Ejecutar DESPUÉS de iniciar el servidor por primera vez
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from models import db, Usuario

def init_admin_user():
    """Crear usuario administrador si no existe"""
    app = create_app()
    
    with app.app_context():
        # Verificar si el usuario admin ya existe
        admin = Usuario.query.filter_by(email='admin@rios.com').first()
        
        if admin:
            print("✅ El usuario administrador ya existe")
            print(f"   Email: {admin.email}")
            print(f"   Nombre: {admin.nombre}")
            return
        
        # Crear usuario admin
        admin = Usuario(
            nombre='Administrador',
            email='admin@rios.com',
            rol='admin'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("=" * 60)
        print("✅ Usuario administrador creado exitosamente")
        print("=" * 60)
        print(f"Email: admin@rios.com")
        print(f"Password: admin123")
        print(f"Rol: admin")
        print("=" * 60)

if __name__ == '__main__':
    init_admin_user()
