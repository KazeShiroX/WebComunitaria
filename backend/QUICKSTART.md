# 🚀 Inicio Rápido - WebComunitaria Backend

Esta guía te ayudará a poner en marcha el backend rápidamente.

## Pasos Rápidos

### 1. Configurar el proyecto

```bash
cd backend
./setup.sh
```

### 2. Configurar MySQL

Edita el archivo `.env` con tus credenciales de MySQL:

```bash
nano .env  # o usa tu editor favorito
```

Ejemplo:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=webcomunitaria
```

### 3. Crear la base de datos

```bash
mysql -u root -p < init_db.sql
```

### 4. Activar entorno virtual e instalar dependencias

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Iniciar el servidor

```bash
python app.py
```

El servidor estará en: `http://localhost:8000`

### 6. Crear usuario administrador

En otra terminal, con el servidor corriendo:

```bash
cd backend
source venv/bin/activate
python init_user.py
```

Credenciales creadas:
- **Email**: admin@rios.com
- **Password**: admin123

### 7. Cargar noticias de ejemplo (Opcional)

```bash
python init_data.py
```

## ✅ Verificación

Visita `http://localhost:8000` - Deberías ver:
```json
{
  "message": "API Web Comunitaria - Backend funcionando correctamente"
}
```

## 🔥 Comandos Rápidos

| Acción | Comando |
|--------|---------|
| Iniciar servidor | `python app.py` |
| Crear admin | `python init_user.py` |
| Cargar datos | `python init_data.py` |
| Generar hash | `python generate_hash.py` |

## 🐛 Problemas Comunes

**Error de conexión a MySQL**
```bash
# Verificar que MySQL esté corriendo
mysql.server status

# Iniciar MySQL si está detenido
mysql.server start
```

**Module not found**
```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

## 📱 Probar con el Frontend Angular

1. El backend debe estar corriendo en `http://localhost:8000`
2. Inicia el frontend Angular en `http://localhost:4200`
3. Usa las credenciales: `admin@rios.com` / `admin123`

---

Para más detalles, consulta [README.md](README.md)
