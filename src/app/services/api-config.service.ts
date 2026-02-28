import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiConfig {
  // Railway detecta automáticamente o usa localhost
  baseUrl = environment.apiUrl || 'http://localhost:8000/api';

  getImageUrl(imagePath: string): string {
    if (!imagePath) return '';
    // Si ya es una URL absoluta (http://, https://, data:image...), la devolvemos tal cual
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://') || imagePath.startsWith('data:')) {
      return imagePath;
    }

    // Si es una ruta relativa, le anteponemos el dominio del backend
    // Removemos '/api' del baseUrl para obtener la raíz del backend
    const backendRoot = this.baseUrl.replace(/\/api\/?$/, '');

    // Aseguramos que la ruta comience con '/'
    const path = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;

    return `${backendRoot}${path}`;
  }
}
