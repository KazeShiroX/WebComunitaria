import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, of, map } from 'rxjs';
import { Usuario, LoginRequest, RegisterRequest } from '../models/usuario.model';
import { ApiConfig } from './api-config.service';

interface AuthResponse {
  usuario: Usuario;
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiConfig = inject(ApiConfig);
  
  private baseUrl = `${this.apiConfig.baseUrl}/auth`;
  
  private usuarioActual = signal<Usuario | null>(null);
  private token = signal<string | null>(null);

  isLoggedIn = computed(() => this.usuarioActual() !== null);
  isAdmin = computed(() => this.usuarioActual()?.rol === 'admin');
  usuario = computed(() => this.usuarioActual());

  constructor() {
    // Cargar usuario y token de localStorage si existe
    const usuarioGuardado = localStorage.getItem('usuario');
    const tokenGuardado = localStorage.getItem('token');
    if (usuarioGuardado && tokenGuardado) {
      this.usuarioActual.set(JSON.parse(usuarioGuardado));
      this.token.set(tokenGuardado);
    }
  }

  getToken(): string | null {
    return this.token();
  }

  login(credentials: LoginRequest): Observable<{ success: boolean; message: string }> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/login`, credentials).pipe(
      tap(response => {
        this.usuarioActual.set(response.usuario);
        this.token.set(response.access_token);
        localStorage.setItem('usuario', JSON.stringify(response.usuario));
        localStorage.setItem('token', response.access_token);
      }),
      map(() => ({ success: true, message: 'Inicio de sesión exitoso' })),
      catchError(error => {
        const message = error.error?.detail || 'Credenciales incorrectas';
        return of({ success: false, message });
      })
    );
  }

  register(data: RegisterRequest): Observable<{ success: boolean; message: string }> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/register`, data).pipe(
      tap(response => {
        this.usuarioActual.set(response.usuario);
        this.token.set(response.access_token);
        localStorage.setItem('usuario', JSON.stringify(response.usuario));
        localStorage.setItem('token', response.access_token);
      }),
      map(() => ({ success: true, message: 'Registro exitoso' })),
      catchError(error => {
        const message = error.error?.detail || 'Error al registrar';
        return of({ success: false, message });
      })
    );
  }

  logout(): void {
    this.usuarioActual.set(null);
    this.token.set(null);
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
  }

  getUsuarioActual(): Usuario | null {
    return this.usuarioActual();
  }

  // Verificar token con el backend
  verificarToken(): Observable<boolean> {
    if (!this.token()) {
      return of(false);
    }
    
    return this.http.get<Usuario>(`${this.baseUrl}/me`).pipe(
      tap(usuario => this.usuarioActual.set(usuario)),
      map(() => true),
      catchError(() => {
        this.logout();
        return of(false);
      })
    );
  }
}
