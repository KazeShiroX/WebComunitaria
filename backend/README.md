# Web Comunitaria - Backend

Backend API para la aplicación Web Comunitaria de Juan José Ríos.

## 🚀 Deployment

### Railway (Producción)

Ver [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) para instrucciones completas de deployment en Railway.

**Resumen rápido:**
1. Crear proyecto en Railway con MySQL
2. Conectar repositorio GitHub
3. Configurar variables de entorno
4. Ejecutar `railway run python init_railway.py`

### Local (Desarrollo)

```bash
# 1. Configurar
./setup.sh

# 2. Crear base de datos
mysql -u root -p < init_db.sql

# 3. Inicializar datos
source venv/bin/activate
python init_user.py
python init_data.py

# 4. Ejecutar
python app.py
```

## � Tecnologías

- **Framework**: Flask 3.0
- **Base de Datos**: MySQL con SQLAlchemy
- **Autenticación**: JWT
- **Servidor Producción**: Gunicorn

## 🌐 URLs Importantes

- **Local**: http://localhost:8000
- **Health Check**: `/api/health`
- **Documentación** completa en los archivos README

## 🔐 Variables de Entorno

```
DATABASE_URL=mysql://user:pass@host:port/db  # Railway automático
SECRET_KEY=tu-clave-secreta
CORS_ORIGINS=https://tu-frontend.com,http://localhost:4200
PORT=8000
```

Ver `.env.example` para más detalles.
