from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Subir una imagen"""
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se envió ningún archivo'}), 400
        
        file = request.files['file']
        
        # Verificar que el archivo tiene nombre
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Verificar extensión
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de archivo no permitido. Solo: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # Verificar tamaño (Flask ya limita, pero lo verificamos también)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        if file_length > MAX_FILE_SIZE:
            return jsonify({'error': 'El archivo es demasiado grande. Máximo 5MB'}), 400
        file.seek(0)
        
        # Generar nombre único para el archivo
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        
        # Guardar el archivo
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Generar URL para acceder a la imagen
        image_url = f"http://localhost:8000/uploads/{unique_filename}"
        
        return jsonify({
            'url': image_url,
            'filename': unique_filename,
            'message': 'Imagen subida exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al subir la imagen: {str(e)}'}), 500
