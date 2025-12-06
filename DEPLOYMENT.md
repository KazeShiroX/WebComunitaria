# 🚀 Guía de Deployment - Web Comunitaria

Guía completa para deployar tu aplicación en Railway (Backend + Frontend).

---

## 📋 Lo que necesitas

- ✅ Cuenta en [Railway](https://railway.app) (gratis)
- ✅ Cuenta de GitHub
- ✅ Git instalado

---

## 🎯 PARTE 1: BACKEND

### Paso 1: Crear Base de Datos en Railway

1. **Inicia sesión en Railway** → [railway.app](https://railway.app)
2. Click **"New Project"**
3. Selecciona **"Provision MySQL"**
4. Railway crea la base de datos automáticamente
5. Click en el servicio MySQL → **Variables** → Copia `DATABASE_URL`

### Paso 2: Subir Backend a GitHub

```bash
cd backend

# Inicializar git
git init
git add .
git commit -m "Backend ready"

# Crear repo en GitHub y pushear
git remote add origin https://github.com/TU_USUARIO/WebComunitaria-Backend.git
git branch -M main
git push -u origin main
```

### Paso 3: Deploy Backend en Railway

1. En Railway, click **"+ New"** → **"GitHub Repo"**
2. Autoriza GitHub y selecciona tu repo del backend
3. Click en el servicio → **Variables** → **"+ Add Variable"**

Agrega estas 3 variables:

```env
DATABASE_URL = <pega el valor de MySQL aquí>
SECRET_KEY = cambia-esto-por-algo-super-secreto-123456
CORS_ORIGINS = http://localhost:4200
```

4. Espera 2-3 minutos a que termine el deploy
5. Click **"Settings"** → **"Generate Domain"**
6. Copia tu URL (ej: `https://tu-backend.up.railway.app`)

### Paso 4: Inicializar Base de Datos

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login y conectar
railway login
cd backend
railway link

# Crear admin y datos de ejemplo
railway run python init_railway.py
```

### Paso 5: Verificar Backend

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

### Paso 2: Subir a GitHub

```bash
cd ..  # Volver a la raíz del proyecto

git add .
git commit -m "Frontend ready for Railway"
git push
```

Si no tiene git inicializado:

```bash
git init
git add .
git commit -m "Frontend ready"
git remote add origin https://github.com/TU_USUARIO/WebComunitaria-Frontend.git
git branch -M main
git push -u origin main
```

### Paso 3: Deploy Frontend en Railway

1. En tu proyecto Railway, click **"+ New"** → **"GitHub Repo"**
2. Selecciona el repo del frontend
3. Railway detecta automáticamente:
   - `package.json`
   - `railway.json`
   - Hace `npm install`
   - Hace `ng build --configuration production`
   - Inicia `node server.js`
4. Click **"Settings"** → **"Generate Domain"**
5. Copia la URL (ej: `https://webcomunitaria.up.railway.app`)

### Paso 4: Actualizar CORS

1. Vuelve al **servicio Backend** en Railway
2. Click **Variables** → Edita `CORS_ORIGINS`:

```env
CORS_ORIGINS = https://tu-frontend.up.railway.app,http://localhost:4200
```

3. Railway redesplegará automáticamente ✅

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

## 📁 ESTRUCTURA RAILWAY

```
Tu Proyecto Railway
│
├── 📦 MySQL Database
│   └── Base de datos webcomunitaria
│
├── 🐍 Backend (Python/Flask)
│   ├── URL: tu-backend.up.railway.app
│   └── Variables: DATABASE_URL, SECRET_KEY, CORS_ORIGINS
│
└── 🎨 Frontend (Angular/Express)
    ├── URL: tu-frontend.up.railway.app
    └── Conecta con: tu-backend.up.railway.app/api
```

---

## 🔄 ACTUALIZAR TU APP

### Backend
```bash
cd backend
git add .
git commit -m "Update backend"
git push
```
✅ Railway auto-redeploy

### Frontend
```bash
git add .
git commit -m "Update frontend"
git push
```
✅ Railway auto-redeploy

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
