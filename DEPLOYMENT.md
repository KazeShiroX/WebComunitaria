# 🚀 Guía de Deployment - Web Comunitaria

Guía completa para deployar tu aplicación en Railway (Backend + Frontend) desde **un solo repositorio**.

---

## 📋 Lo que necesitas

- ✅ Cuenta en [Railway](https://railway.app) (gratis)
- ✅ Cuenta de GitHub
- ✅ Git instalado

---

## 📦 PASO 0: SUBIR TODO A GITHUB (UNA SOLA VEZ)

Tu proyecto ya está en un solo repositorio, ¡perfecto! Solo súbelo a GitHub:

```bash
# Desde la raíz del proyecto (WebComunitaria)
git init
git add .
git commit -m "Web Comunitaria completa - ready for Railway"

# Crear repo en GitHub (hazlo desde github.com)
# Luego conecta y sube:
git remote add origin https://github.com/TU_USUARIO/WebComunitaria.git
git branch -M main
git push -u origin main
```

✅ Ahora tienes todo en GitHub: backend/ y frontend en el mismo repo

---

## 🎯 PARTE 1: BACKEND

### Paso 1: Crear Base de Datos en Railway

1. **Inicia sesión en Railway** → [railway.app](https://railway.app)
2. Click **"New Project"**
3. Selecciona **"Provision MySQL"**
4. Railway crea la base de datos automáticamente
5. Click en el servicio MySQL → **Variables** → Copia `DATABASE_URL`

### Paso 2: Deploy Backend

1. En Railway, click **"+ New"** → **"GitHub Repo"**
2. Autoriza GitHub y selecciona tu repo **WebComunitaria**
3. ⚠️ **IMPORTANTE**: Railway va a intentar deployar todo el repo
4. Click en el servicio que se creó → **Settings**
5. Busca **"Root Directory"** y cambia a: **`backend`**
6. Click **"Save"**

Railway ahora solo verá la carpeta `backend/` 🎯

### Paso 3: Configurar Variables

Click **Variables** → **"+ Add Variable"**

Agrega estas 3 variables:

```env
DATABASE_URL = <pega el valor de MySQL aquí>
SECRET_KEY = cambia-esto-por-algo-super-secreto-123456
CORS_ORIGINS = http://localhost:4200
```

### Paso 4: Generar Dominio

1. Click **"Settings"** → **"Generate Domain"**
2. Copia tu URL (ej: `https://webcomunitaria-backend.up.railway.app`)

### Paso 5: Inicializar Base de Datos

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login y conectar al BACKEND
railway login
cd backend
railway link

# Crear admin y datos de ejemplo
railway run python init_railway.py
```

### Paso 6: Verificar Backend

Visita: `https://tu-backend.up.railway.app/api/health`

Deberías ver: `{"status": "healthy"}` ✅

---

## 🎨 PARTE 2: FRONTEND

### Paso 1: Configurar URL del Backend

Edita `src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://TU-BACKEND.up.railway.app/api'  // ← Cambia esto
};
```

Commit y push:

```bash
# Desde la raíz del proyecto
git add .
git commit -m "Configure production backend URL"
git push
```

### Paso 2: Deploy Frontend

1. En tu proyecto Railway (el mismo donde está el backend), click **"+ New"**
2. Selecciona **"GitHub Repo"**
3. Busca y selecciona tu repo **WebComunitaria** (el mismo)
4. ⚠️ **IMPORTANTE**: Railway detectará el mismo repo
5. Click en el nuevo servicio → **Settings**
6. Busca **"Root Directory"** y cambia a: **`.`** (punto = raíz)
   - Esto hace que Railway vea el frontend en la raíz del proyecto
7. Click **"Save"**

Railway ahora deployará el frontend desde la raíz 🎯

### Paso 3: Generar Dominio

1. Click **"Settings"** → **"Generate Domain"**
2. Copia la URL (ej: `https://webcomunitaria.up.railway.app`)

### Paso 4: Actualizar CORS

1. Vuelve al **servicio Backend** en Railway
2. Click **Variables** → Edita `CORS_ORIGINS`:

```env
CORS_ORIGINS = https://webcomunitaria.up.railway.app,http://localhost:4200
```

3. Railway redesplegará el backend automáticamente ✅

---

## ✅ VERIFICACIÓN

### 1. Backend
```
https://tu-backend.up.railway.app/api/health
→ {"status": "healthy"}
```

### 2. Frontend
```
https://tu-frontend.up.railway.app
→ Página visible
```

### 3. Login
- Email: `admin@webcomunitaria.com`
- Password: `admin123`

### 4. Funcionalidades
- ✅ Ver noticias
- ✅ Buscar y filtrar
- ✅ Login
- ✅ Crear/editar/eliminar noticias
- ✅ Subir imágenes

---

## 📁 ESTRUCTURA RAILWAY (MONOREPO)

```
Railway Proyecto: WebComunitaria
│
├── 📦 MySQL Database
│   └── Base de datos webcomunitaria
│
├── 🐍 Backend Service
│   ├── Repo: WebComunitaria
│   ├── Root Directory: backend/
│   ├── URL: tu-backend.up.railway.app
│   └── Variables: DATABASE_URL, SECRET_KEY, CORS_ORIGINS
│
└── 🎨 Frontend Service
    ├── Repo: WebComunitaria (mismo repo!)
    ├── Root Directory: . (raíz)
    ├── URL: tu-frontend.up.railway.app
    └── Conecta con: tu-backend.up.railway.app/api
```

**Clave**: Mismo repo, diferente "Root Directory" para cada servicio ✅

---

## 🔄 ACTUALIZAR TU APP

Como todo está en un solo repo:

```bash
# Haz tus cambios en backend/ o en el frontend
git add .
git commit -m "Update: descripción de cambios"
git push
```

✅ Railway auto-redeploy de **ambos servicios** (backend y frontend)

**Tip**: Si solo cambiaste el backend, Railway solo redesplegará el backend. Lo mismo para el frontend.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ "Database connection failed"
**Solución:** Verifica que `DATABASE_URL` esté en Variables del backend

### ❌ "CORS policy blocked"
**Solución:** 
1. Agrega tu URL de frontend a `CORS_ORIGINS` en el backend
2. Formato: `https://tu-frontend.up.railway.app,http://localhost:4200`

### ❌ Frontend carga pero sin datos
**Solución:**
1. F12 → Console → Ver errores
2. Verifica que `environment.prod.ts` tenga la URL correcta del backend
3. Confirma que backend esté activo: visita `/api/health`

### ❌ Error 404 en rutas
**Solución:** Verifica que `server.js` tenga el catch-all: `app.get('*', ...)`

### ⚠️ Imágenes desaparecen
**Explicación:** Railway usa almacenamiento temporal. Para persistencia:
- Railway Volumes
- Cloudinary
- AWS S3

---

## 💰 COSTOS

**Plan Gratuito**: $5 USD/mes de crédito

**Uso típico:**
- MySQL: ~$3/mes
- Backend: ~$1/mes
- Frontend: ~$1/mes
- **Total: ~$5/mes** ✅ Gratis

---

## 📌 COMANDOS ÚTILES

```bash
# Railway CLI
railway login                          # Autenticar
railway link                           # Conectar proyecto
railway logs                           # Ver logs
railway run python init_railway.py     # Ejecutar script
railway env                            # Ver variables

# Verificación
curl https://tu-backend.up.railway.app/api/health
```

---

## 🔐 SEGURIDAD

Antes de lanzar públicamente:

1. ✅ Cambia `SECRET_KEY` a algo único
2. ✅ Cambia contraseña del admin
3. ✅ Revisa `CORS_ORIGINS` (solo tus dominios)
4. ✅ Habilita backups de Railway

---

## 🎉 ¡LISTO!

Tu aplicación está en la nube:

- 🌐 **Frontend**: https://tu-app.up.railway.app
- 🔧 **Backend**: https://tu-backend.up.railway.app/api
- 👤 **Admin**: admin@webcomunitaria.com / admin123

---

## 📞 SOPORTE

Si tienes problemas:

1. Revisa logs en Railway Dashboard
2. Verifica que todas las variables estén configuradas
3. Asegúrate que los dominios en CORS sean correctos
4. Consulta [Railway Docs](https://docs.railway.app)

---

**¡Tu Web Comunitaria está 100% online! 🚀**
