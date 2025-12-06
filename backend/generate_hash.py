#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de prueba
"""
from werkzeug.security import generate_password_hash

# Generar hash de contraseña para el usuario admin
password = "admin123"
password_hash = generate_password_hash(password)

print("=" * 60)
print("HASH DE CONTRASEÑA PARA USUARIO ADMIN")
print("=" * 60)
print(f"Contraseña: {password}")
print(f"Hash: {password_hash}")
print("=" * 60)
print("\nCopia este hash y úsalo en el archivo init_db.sql")
print("para el INSERT del usuario administrador.")
