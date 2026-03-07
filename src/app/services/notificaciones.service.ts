import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of, tap, interval, switchMap } from 'rxjs';
import { ApiConfig } from './api-config.service';
import { AuthService } from './auth.service';

export interface Notificacion {
    id: number;
    usuario_id: number;
    noticia_id: number | null;
    mensaje: string;
    leida: boolean;
    fecha: string;
}

@Injectable({
    providedIn: 'root'
})
export class NotificacionesService {
    private http = inject(HttpClient);
    private apiConfig = inject(ApiConfig);
    private authService = inject(AuthService);

    private _notificaciones = signal<Notificacion[]>([]);
    private _noLeidas = signal<number>(0);

    notificaciones = this._notificaciones.asReadonly();
    noLeidas = this._noLeidas.asReadonly();

    private get baseUrl() {
        return `${this.apiConfig.baseUrl}/auth/notificaciones`;
    }

    cargar(): void {
        if (!this.authService.isLoggedIn()) return;

        this.http.get<{ items: Notificacion[]; no_leidas: number }>(this.baseUrl)
            .pipe(catchError(() => of({ items: [], no_leidas: 0 })))
            .subscribe(res => {
                this._notificaciones.set(res.items);
                this._noLeidas.set(res.no_leidas);
            });
    }

    marcarLeida(id: number): Observable<any> {
        return this.http.post(`${this.baseUrl}/${id}/leer`, {}).pipe(
            tap(() => {
                this._notificaciones.update(lista =>
                    lista.map(n => n.id === id ? { ...n, leida: true } : n)
                );
                this._noLeidas.update(v => Math.max(0, v - 1));
            }),
            catchError(() => of(null))
        );
    }

    marcarTodasLeidas(): Observable<any> {
        return this.http.post(`${this.baseUrl}/leer-todas`, {}).pipe(
            tap(() => {
                this._notificaciones.update(lista =>
                    lista.map(n => ({ ...n, leida: true }))
                );
                this._noLeidas.set(0);
            }),
            catchError(() => of(null))
        );
    }
}
