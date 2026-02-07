from app import create_app
from models import db, Noticia, Usuario
from datetime import datetime

def init_data():
    app = create_app()
    with app.app_context():
        # Obtener usuario admin
        admin = Usuario.query.filter_by(email='admin@rios.com').first()
        if not admin:
            print("❌ Error: Debes crear el usuario admin primero (run init_user.py)")
            return

        # Verificar si ya hay noticias
        if Noticia.query.count() > 0:
            print("✅ Ya existen noticias en la base de datos")
            return

        # Crear noticias de ejemplo
        noticias_ejemplo = [
            {
                'titulo': 'Gran Posada Navideña en JJR',
                'descripcion': 'Celebración navideña para los niños de la comunidad.',
                'contenido': 'La Facultad de Agricultura del Valle del Fuerte organizó una hermosa posada para los niños de Juan José Ríos. Hubo regalos, dulces, piñatas y mucha diversión. El evento contó con la participación de estudiantes y maestros.',
                'categoria': 'Eventos',
                'imagen': 'https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=800&q=80',
                'autor_id': admin.id
            },
            {
                'titulo': 'Campaña de Limpieza Comunitaria',
                'descripcion': 'Únete a nosotros para mantener limpia nuestra ciudad.',
                'contenido': 'Este próximo sábado tendremos una jornada de limpieza en el parque central. Invitamos a todos los vecinos a participar traer sus escobas. Juntos podemos hacer de Juan José Ríos un lugar más limpio.',
                'categoria': 'Comunidad',
                'imagen': 'https://images.unsplash.com/photo-1550989460-0adf9ea622e2?w=800&q=80',
                'autor_id': admin.id
            },
            {
                'titulo': 'Nuevo Curso de Computación Gratuito',
                'descripcion': 'Aprende habilidades digitales básicas.',
                'contenido': 'Inician las inscripciones para el curso básico de computación en la biblioteca municipal. Horarios flexibles y certificado al finalizar. ¡No te lo pierdas!',
                'categoria': 'Educación',
                'imagen': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&q=80',
                'autor_id': admin.id
            }
        ]

        for n in noticias_ejemplo:
            noticia = Noticia(**n)
            db.session.add(noticia)
        
        db.session.commit()
        print(f"✅ Se insertaron {len(noticias_ejemplo)} noticias de ejemplo")

if __name__ == '__main__':
    init_data()
