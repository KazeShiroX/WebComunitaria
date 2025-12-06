#!/usr/bin/env python3
"""
Script de inicialización completa para Railway
Ejecuta: railway run python init_railway.py
"""

import sys
from init_user import main as init_user
from init_data import main as init_data

def main():
    print("🚀 Inicializando base de datos en Railway...")
    print("\n📝 Paso 1: Creando usuario administrador...")
    
    try:
        init_user()
        print("✅ Usuario admin creado exitosamente")
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        return False
    
    print("\n📰 Paso 2: Cargando noticias de ejemplo...")
    try:
        init_data()
        print("✅ Noticias de ejemplo cargadas exitosamente")
    except Exception as e:
        print(f"❌ Error cargando noticias: {e}")
        return False
    
    print("\n🎉 ¡Inicialización completada!")
    print("\n📌 Credenciales de admin:")
    print("   Email: admin@webcomunitaria.com")
    print("   Password: admin123")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
