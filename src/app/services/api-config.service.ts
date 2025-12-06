import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiConfig {
  readonly baseUrl = 'http://localhost:8000/api';
}
