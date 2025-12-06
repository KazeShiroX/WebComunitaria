import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiConfig {
  // Railway detecta automáticamente o usa localhost
  baseUrl = environment.apiUrl || 'http://localhost:8000/api';
}
