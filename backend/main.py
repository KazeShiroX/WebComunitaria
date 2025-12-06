from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import init_db, async_session
from models import Usuario, Noticia, RolEnum
from auth import get_password_hash
from routers.auth_router import router as auth_router
from routers.noticias_router import router as noticias_router
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar DB y crear datos de prueba
    await init_db()
    await create_initial_data()
    yield
    # Shutdown

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST para el portal de noticias comunitarias Ríos Informa",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(noticias_router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Ríos Informa",
        "docs": "/docs",
        "version": settings.APP_VERSION
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

async def create_initial_data():
    """Crear usuario admin y noticias de prueba si no existen"""
    async with async_session() as db:
        # Verificar si ya existe el admin
        result = await db.execute(select(Usuario).where(Usuario.email == "admin@rios.com"))
        admin = result.scalar_one_or_none()
        
        if not admin:
            # Crear admin
            admin = Usuario(
                nombre="Administrador",
                email="admin@rios.com",
                password_hash=get_password_hash("admin123"),
                rol=RolEnum.admin,
                avatar="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop&crop=face"
            )
            db.add(admin)
            await db.commit()
            await db.refresh(admin)
            
            # Crear noticias de prueba
            noticias_data = [
                {
                    "titulo": "Nuevo parque comunitario abre sus puertas en Ríos",
                    "descripcion": "El nuevo espacio verde cuenta con áreas de juego, canchas deportivas y zonas de descanso para el disfrute de todos los residentes.",
                    "contenido": "El nuevo espacio verde cuenta con áreas de juego, canchas deportivas y zonas de descanso para el disfrute de todos los residentes. Este parque representa una inversión significativa en la calidad de vida de nuestra comunidad.",
                    "categoria": "Noticias Locales",
                    "imagen": "https://images.unsplash.com/photo-1588714477688-cf28a50e94f7?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Equipo de béisbol local avanza a la final del torneo regional",
                    "descripcion": "Después de una emocionante semifinal, el equipo de béisbol de Ríos se prepara para competir por el campeonato.",
                    "contenido": "Después de una emocionante semifinal, el equipo de béisbol de Ríos se prepara para competir por el campeonato. Los jugadores han demostrado un excelente rendimiento durante toda la temporada.",
                    "categoria": "Deportes",
                    "imagen": "https://images.unsplash.com/photo-1529768167801-9173d94c2a42?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Festival de arte y cultura atrae a visitantes de toda la región",
                    "descripcion": "El evento incluyó exposiciones de arte, presentaciones musicales y danzas folclóricas, celebrando la riqueza cultural de Ríos.",
                    "contenido": "El evento incluyó exposiciones de arte, presentaciones musicales y danzas folclóricas, celebrando la riqueza cultural de Ríos. Artistas locales e internacionales participaron en esta celebración cultural.",
                    "categoria": "Cultura",
                    "imagen": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Iniciativa ciudadana limpia y embellece el centro de Ríos",
                    "descripcion": "Voluntarios se unieron para pintar fachadas, plantar árboles y mejorar el aspecto del centro de la ciudad.",
                    "contenido": "Voluntarios se unieron para pintar fachadas, plantar árboles y mejorar el aspecto del centro de la ciudad. Esta iniciativa demuestra el compromiso de la comunidad con su entorno.",
                    "categoria": "Comunidad",
                    "imagen": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Nueva biblioteca pública ofrece servicios gratuitos",
                    "descripcion": "La biblioteca cuenta con más de 10,000 libros, computadoras con acceso a internet y programas de lectura para niños.",
                    "contenido": "La biblioteca cuenta con más de 10,000 libros, computadoras con acceso a internet y programas de lectura para niños. Un espacio dedicado al conocimiento y la cultura.",
                    "categoria": "Noticias Locales",
                    "imagen": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Torneo de fútbol juvenil reúne a equipos de la región",
                    "descripcion": "Más de 20 equipos participan en el torneo que busca promover el deporte entre los jóvenes.",
                    "contenido": "Más de 20 equipos participan en el torneo que busca promover el deporte entre los jóvenes. El evento se desarrollará durante todo el mes.",
                    "categoria": "Deportes",
                    "imagen": "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Concierto benéfico recauda fondos para el hospital local",
                    "descripcion": "Artistas locales donaron su talento para ayudar a equipar el área de pediatría del hospital.",
                    "contenido": "Artistas locales donaron su talento para ayudar a equipar el área de pediatría del hospital. Se recaudaron más de $50,000 en una noche memorable.",
                    "categoria": "Comunidad",
                    "imagen": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Exposición de fotografía documenta la historia de Ríos",
                    "descripcion": "Imágenes históricas muestran la evolución de nuestra ciudad a lo largo de los últimos 100 años.",
                    "contenido": "Imágenes históricas muestran la evolución de nuestra ciudad a lo largo de los últimos 100 años. La exposición estará disponible hasta fin de mes.",
                    "categoria": "Cultura",
                    "imagen": "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Programa de reciclaje se expande a nuevos vecindarios",
                    "descripcion": "El municipio amplía el programa de recolección selectiva de residuos a 15 nuevas colonias.",
                    "contenido": "El municipio amplía el programa de recolección selectiva de residuos a 15 nuevas colonias. Los vecinos recibirán contenedores especiales para separar sus desechos.",
                    "categoria": "Noticias Locales",
                    "imagen": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Maratón comunitario promueve estilos de vida saludables",
                    "descripcion": "Más de 500 corredores participaron en la carrera de 10 kilómetros por las calles de la ciudad.",
                    "contenido": "Más de 500 corredores participaron en la carrera de 10 kilómetros por las calles de la ciudad. El evento contó con categorías para todas las edades.",
                    "categoria": "Deportes",
                    "imagen": "https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Feria gastronómica celebra la cocina tradicional",
                    "descripcion": "Cocineros locales presentaron platillos típicos de la región en un evento que reunió a miles de visitantes.",
                    "contenido": "Cocineros locales presentaron platillos típicos de la región en un evento que reunió a miles de visitantes. La feria se convirtió en un éxito rotundo.",
                    "categoria": "Cultura",
                    "imagen": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=250&fit=crop"
                },
                {
                    "titulo": "Vecinos organizan patrullas de vigilancia comunitaria",
                    "descripcion": "En coordinación con la policía local, los residentes implementan un programa de seguridad vecinal.",
                    "contenido": "En coordinación con la policía local, los residentes implementan un programa de seguridad vecinal. La iniciativa ha reducido los índices de delincuencia en la zona.",
                    "categoria": "Comunidad",
                    "imagen": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=400&h=250&fit=crop"
                }
            ]
            
            for noticia_data in noticias_data:
                noticia = Noticia(**noticia_data, autor_id=admin.id)
                db.add(noticia)
            
            await db.commit()
            print("✅ Datos iniciales creados correctamente")
