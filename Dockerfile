FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el backend completo (incluye public/ con el frontend)
COPY backend/ ./

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["python", "app.py"]