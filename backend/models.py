from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('admin', 'moderador', 'usuario'), default='usuario', nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    noticias = db.relationship('Noticia', backref='autor_obj', lazy=True, cascade='all, delete-orphan')
    comentarios = db.relationship('Comentario', backref='usuario_obj', lazy=True, cascade='all, delete-orphan')
    reacciones = db.relationship('Reaccion', backref='usuario_obj', lazy=True, cascade='all, delete-orphan')
    notificaciones = db.relationship('Notificacion', backref='usuario_obj', lazy=True, cascade='all, delete-orphan')
    eventos = db.relationship('Evento', backref='autor_obj', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hashear la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'avatar': self.avatar
        }


class Noticia(db.Model):
    __tablename__ = 'noticias'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    contenido = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(500), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    comentarios = db.relationship('Comentario', backref='noticia_obj', lazy=True, cascade='all, delete-orphan')
    reacciones = db.relationship('Reaccion', backref='noticia_obj', lazy=True, cascade='all, delete-orphan')
    notificaciones = db.relationship('Notificacion', backref='noticia_notif_obj', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'contenido': self.contenido or '',
            'categoria': self.categoria,
            'imagen': self.imagen or 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=250&fit=crop',
            'fecha': self.fecha.isoformat(),
            'autor_id': self.autor_id,
            'autor_nombre': self.autor_obj.nombre if self.autor_obj else 'Desconocido'
        }


class Comentario(db.Model):
    __tablename__ = 'comentarios'
    
    id = db.Column(db.Integer, primary_key=True)
    noticia_id = db.Column(db.Integer, db.ForeignKey('noticias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'noticia_id': self.noticia_id,
            'usuario_id': self.usuario_id,
            'usuario_nombre': self.usuario_obj.nombre if self.usuario_obj else 'Desconocido',
            'usuario_avatar': self.usuario_obj.avatar if self.usuario_obj else None,
            'texto': self.texto,
            'fecha': self.fecha.isoformat()
        }


class Reaccion(db.Model):
    __tablename__ = 'reacciones'
    
    id = db.Column(db.Integer, primary_key=True)
    noticia_id = db.Column(db.Integer, db.ForeignKey('noticias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.Enum('like', 'love', 'wow', 'sad', 'angry'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Restricción única: un usuario solo puede reaccionar una vez por noticia
    __table_args__ = (
        db.UniqueConstraint('noticia_id', 'usuario_id', name='uq_reaccion_usuario_noticia'),
    )
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'noticia_id': self.noticia_id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'fecha': self.fecha.isoformat()
        }


class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    noticia_id = db.Column(db.Integer, db.ForeignKey('noticias.id'), nullable=True)
    mensaje = db.Column(db.String(300), nullable=False)
    leida = db.Column(db.Boolean, default=False, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'noticia_id': self.noticia_id,
            'mensaje': self.mensaje,
            'leida': self.leida,
            'fecha': self.fecha.isoformat()
        }


class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False, default='General')
    fecha_evento = db.Column(db.DateTime, nullable=False)   # Fecha del evento
    imagen = db.Column(db.String(500), nullable=True)
    lugar = db.Column(db.String(200), nullable=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        from datetime import date
        hoy = date.today()
        fecha_ev = self.fecha_evento.date()
        dias = (fecha_ev - hoy).days

        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'fecha_evento': self.fecha_evento.isoformat(),
            'imagen': self.imagen or '',
            'lugar': self.lugar or '',
            'autor_id': self.autor_id,
            'autor': self.autor_obj.nombre if self.autor_obj else 'Desconocido',
            'created_at': self.created_at.isoformat(),
            'dias_restantes': dias   # negativo = pasado, 0 = hoy, positivo = próximo
        }

