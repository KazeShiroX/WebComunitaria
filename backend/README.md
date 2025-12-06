# Backend - API de Noticias Comunitarias

API REST desarrollada con FastAPI para el portal de noticias comunitarias "Ríos Informa".

## Requisitos

- Python 3.9+
- pip

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
uvicorn main:app --reload --port 8000
```

El servidor estará disponible en: http://localhost:8000

## Documentación API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints principales

### Noticias
- `GET /api/noticias` - Listar noticias con paginación
- `GET /api/noticias/{id}` - Obtener una noticia
- `POST /api/noticias` - Crear noticia (requiere autenticación)
- `PUT /api/noticias/{id}` - Actualizar noticia (requiere autenticación)
- `DELETE /api/noticias/{id}` - Eliminar noticia (requiere autenticación)

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `GET /api/auth/me` - Obtener usuario actual

## Credenciales de prueba

- Email: admin@rios.com
- Password: admin123
