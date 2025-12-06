# Backend WebComunitaria

Backend API REST desarrollado con Flask y MySQL para la aplicación WebComunitaria.

## 🚀 Características

- **Autenticación JWT**: Sistema completo de login/registro con tokens
- **CRUD de Noticias**: Gestión completa de noticias
- **Paginación**: Soporte para paginación de noticias
- **Filtros**: Filtrado por categoría y búsqueda
- **CORS**: Configurado para trabajar con Angular

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Configurar el entorno virtual

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar MySQL

Primero, inicia MySQL y ejecuta el script de inicialización:

```bash
mysql -u root -p < init_db.sql
```

O manualmente:
```bash
mysql -u root -p
```

Luego dentro de MySQL:
```sql
source init_db.sql;
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y edita con tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de MySQL:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=webcomunitaria
SECRET_KEY=cambia_esto_por_una_clave_segura
```

## ▶️ Ejecutar el servidor

### 1. Iniciar el servidor Flask

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:8000`

### 2. Crear usuario administrador

**IMPORTANTE**: El servidor debe estar corriendo para ejecutar este paso.

En otra terminal:

```bash
cd backend
source venv/bin/activate  # Activar el entorno virtual
python init_user.py
```

Esto creará el usuario administrador con:
- **Email**: admin@rios.com
- **Password**: admin123

### 3. Cargar noticias de ejemplo (Opcional)

```bash
python init_data.py
```

## 📡 Endpoints de la API

### Autenticación

- **POST** `/api/auth/login` - Iniciar sesión
  ```json
  {
    "email": "admin@rios.com",
    "password": "admin123"
  }
  ```

- **POST** `/api/auth/register` - Registrar nuevo usuario
  ```json
  {
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123"
  }
  ```

- **GET** `/api/auth/me` - Obtener usuario actual (requiere token)

### Noticias

- **GET** `/api/noticias` - Obtener noticias con paginación
  - Query params: `pagina`, `items_por_pagina`, `categoria`, `busqueda`

- **GET** `/api/noticias/:id` - Obtener noticia por ID

- **POST** `/api/noticias` - Crear noticia (requiere autenticación)
  ```json
  {
    "titulo": "Título de la noticia",
    "descripcion": "Descripción breve",
    "contenido": "Contenido completo",
    "categoria": "Noticias Locales",
    "imagen": "https://ejemplo.com/imagen.jpg"
  }
  ```

- **PUT** `/api/noticias/:id` - Actualizar noticia (requiere autenticación)

- **DELETE** `/api/noticias/:id` - Eliminar noticia (requiere autenticación)

## 🔐 Credenciales de Prueba

- **Email**: admin@rios.com
- **Password**: admin123

## 🗄️ Estructura de la Base de Datos

### Tabla: usuarios
- id (PK)
- nombre
- email (unique)
- password_hash
- rol (admin/usuario)
- avatar
- fecha_registro

### Tabla: noticias
- id (PK)
- titulo
- descripcion
- contenido
- categoria
- imagen
- fecha
- autor_id (FK → usuarios)

## 📁 Estructura del Proyecto

```
backend/
├── app.py                 # Aplicación principal
├── config.py             # Configuración
├── models.py             # Modelos de base de datos
├── auth.py               # Utilidades de autenticación
├── requirements.txt      # Dependencias
├── .env.example         # Ejemplo de variables de entorno
├── init_db.sql          # Script de inicialización de BD
├── generate_hash.py     # Utilidad para generar hashes
└── routes/
    ├── auth_routes.py   # Rutas de autenticación
    └── noticias_routes.py # Rutas de noticias
```

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica que MySQL esté corriendo: `mysql.server status`
- Verifica las credenciales en el archivo `.env`
- Asegúrate de que la base de datos `webcomunitaria` existe

### Error de importación de módulos
- Asegúrate de tener el entorno virtual activado
- Reinstala las dependencias: `pip install -r requirements.txt`

### CORS errors desde Angular
- Verifica que `http://localhost:4200` esté en `CORS_ORIGINS` en `config.py`

## 📝 Notas

- El backend usa SQLAlchemy ORM para interactuar con MySQL
- Los tokens JWT expiran después de 24 horas
- Todos los usuarios registrados tienen rol 'admin' por defecto
- Las contraseñas se hashean usando Werkzeug Security
