#!/usr/bin/env python3
"""
Script para inicializar noticias de ejemplo en la base de datos
"""
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from models import db, Noticia, Usuario

def init_sample_news():
    """Crear noticias de ejemplo"""
    app = create_app()
    
    with app.app_context():
        # Buscar al administrador
        admin = Usuario.query.filter_by(email='admin@rios.com').first()
        
        if not admin:
            print("❌ Error: Primero debes crear el usuario administrador")
            print("   Ejecuta: python init_user.py")
            return
        
        # Verificar si ya existen noticias
        if Noticia.query.count() > 0:
            print("⚠️  Ya existen noticias en la base de datos")
            return
        
        # Crear noticias de ejemplo
        noticias_ejemplo = [
            {
                'titulo': 'Inauguración del nuevo parque comunitario',
                'descripcion': 'El próximo sábado se inaugurará el parque renovado en el centro de Juan José Ríos',
                'contenido': 'La comunidad de Juan José Ríos se prepara para la inauguración del parque central que ha sido completamente renovado. El evento contará con actividades para toda la familia.',
                'categoria': 'Comunidad',
                'imagen': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=250&fit=crop',
                'fecha': datetime.utcnow() - timedelta(days=1)
            },
            {
                'titulo': 'Torneo de fútbol local este fin de semana',
                'descripcion': 'Se llevará a cabo el torneo anual de fútbol con la participación de 8 equipos',
                'contenido': 'El torneo contará con equipos de todas las edades y habrá premios para los ganadores. El evento se realizará en la cancha municipal.',
                'categoria': 'Deportes',
                'imagen': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=250&fit=crop',
                'fecha': datetime.utcnow() - timedelta(days=2)
            },
            {
                'titulo': 'Festival cultural de primavera',
                'descripcion': 'Un evento lleno de música, danza y arte local',
                'contenido': 'El festival celebrará las tradiciones de nuestra comunidad con presentaciones de grupos locales, exposiciones de arte y comida típica.',
                'categoria': 'Cultura',
                'imagen': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400&h=250&fit=crop',
                'fecha': datetime.utcnow() - timedelta(days=3)
            },
            {
                'titulo': 'Nuevo servicio de recolección de basura',
                'descripcion': 'Mejoras en el sistema de limpieza municipal',
                'contenido': 'A partir del próximo mes, habrá nuevos horarios y más frecuencia en la recolección de basura para mantener nuestra comunidad más limpia.',
                'categoria': 'Noticias Locales',
                'imagen': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=400&h=250&fit=crop',
                'fecha': datetime.utcnow() - timedelta(days=4)
            },
            {
                'titulo': 'Victorias del equipo juvenil de básquetbol',
                'descripcion': 'Nuestro equipo logra importantes triunfos en el torneo regional',
                'contenido': 'El equipo juvenil de Juan José Ríos ha tenido un desempeño excepcional ganando sus últimos tres partidos.',
                'categoria': 'Deportes',
                'imagen': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=250&fit=crop',
                'fecha': datetime.utcnow() - timedelta(days=5)
            },
            {
                'titulo': 'Taller de arte para niños',
                'descripcion': 'Inscripciones abiertas para el taller de verano',
                'contenido': 'La casa de la cultura abre inscripciones para talleres de pintura, dibujo y escultura dirigidos a niños de 6 a 12 años.',
                'categoria': 'Cultura',
                'imagen': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400&h=250&fit=crop',
                'fecha': datetime.utcnow() - timedelta(days=6)
            }
        ]
        
        for noticia_data in noticias_ejemplo:
            noticia = Noticia(
                titulo=noticia_data['titulo'],
                descripcion=noticia_data['descripcion'],
                contenido=noticia_data['contenido'],
                categoria=noticia_data['categoria'],
                imagen=noticia_data['imagen'],
                fecha=noticia_data['fecha'],
                autor_id=admin.id
            )
            db.session.add(noticia)
        
        db.session.commit()
        
        print("=" * 60)
        print(f"✅ Se crearon {len(noticias_ejemplo)} noticias de ejemplo")
        print("=" * 60)

if __name__ == '__main__':
    init_sample_news()
