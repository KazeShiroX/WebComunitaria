from flask import Flask, send_from_directory, request
from flask_cors import CORS
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.noticias_routes import noticias_bp
from routes.upload_routes import upload_bp
import os

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__, static_folder='public', static_url_path='')
    app.config.from_object(Config)
    
    # Configuración para uploads
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    
    # Inicializar extensiones
    db.init_app(app)
    
    # CORS manual para garantizar headers en TODAS las respuestas
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin', '')
        allowed_origins = Config.CORS_ORIGINS
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @app.before_request
    def handle_preflight():
        if request.method == 'OPTIONS':
            origin = request.headers.get('Origin', '')
            if origin in Config.CORS_ORIGINS:
                from flask import make_response
                response = make_response()
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                return response, 204
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(noticias_bp, url_prefix='/api/noticias')
    app.register_blueprint(upload_bp, url_prefix='/api')
    
    # Ruta para servir archivos subidos
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)
    
    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # Ruta raíz informativa
    @app.route('/')
    def index():
        return {'message': 'Backend WebComunitaria funcionando.'}, 200
    
    # Crear tablas y carpeta de uploads si no existen
    with app.app_context():
        db.create_all()
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('public', exist_ok=True)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG if hasattr(Config, 'DEBUG') else False)

