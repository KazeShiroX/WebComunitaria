from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.noticias_routes import noticias_bp
from routes.upload_routes import upload_bp
import os

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuración para uploads
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(noticias_bp, url_prefix='/api/noticias')
    app.register_blueprint(upload_bp, url_prefix='/api')
    
    # Ruta para servir archivos subidos
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return {'message': 'API Web Comunitaria - Backend funcionando correctamente'}, 200
    
    @app.route('/api/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # Crear tablas y carpeta de uploads si no existen
    with app.app_context():
        db.create_all()
        os.makedirs('uploads', exist_ok=True)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
