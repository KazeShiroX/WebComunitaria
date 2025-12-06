#!/bin/bash

echo "=================================================="
echo "  Configurando Backend WebComunitaria"
echo "=================================================="
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales de MySQL"
    echo ""
fi

echo ""
echo "=================================================="
echo "✅ Configuración completada"
echo "=================================================="
echo ""
echo "Próximos pasos:"
echo "1. Edita el archivo .env con tus credenciales de MySQL"
echo "2. Ejecuta el script SQL: mysql -u root -p < init_db.sql"
echo "3. Inicia el servidor: python app.py"
echo ""
