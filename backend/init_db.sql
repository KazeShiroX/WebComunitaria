-- Script de inicialización de base de datos MySQL
-- WebComunitaria

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS webcomunitaria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE webcomunitaria;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'usuario') DEFAULT 'usuario' NOT NULL,
    avatar VARCHAR(255),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de noticias
CREATE TABLE IF NOT EXISTS noticias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    contenido TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    imagen VARCHAR(500),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    autor_id INT NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_categoria (categoria),
    INDEX idx_fecha (fecha),
    INDEX idx_autor (autor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar usuario administrador de prueba (contraseña: admin123)
-- Nota: El hash de contraseña se generará automáticamente cuando uses la API
-- Por ahora, debes ejecutar el script init_user.py después de iniciar el servidor
-- O puedes registrarte usando la API /api/auth/register

-- Insertar noticias de ejemplo
-- Nota: Las noticias se crearán usando el script init_data.py después de crear el usuario admin
