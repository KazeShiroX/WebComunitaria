import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiConfig } from './api-config.service';

export interface Evento {
    id: number;
    titulo: string;
    descripcion: string;
    categoria: string;
    fecha_evento: string;
    imagen: string;
    lugar: string;
    autor: string;
    autor_id: number;
    dias_restantes: number;
    created_at: string;
}

@Injectable({ providedIn: 'root' })
export class EventosService {
    private http = inject(HttpClient);
    private apiConfig = inject(ApiConfig);

    private get base() { return `${this.apiConfig.baseUrl}/eventos`; }

    getEventos(categoria?: string): Observable<Evento[]> {
        let params = new HttpParams();
        if (categoria && categoria !== 'Todos') params = params.set('categoria', categoria);
        return this.http.get<Evento[]>(this.base, { params });
    }

    crearEvento(data: Partial<Evento>): Observable<Evento> {
        const token = localStorage.getItem('token');
        return this.http.post<Evento>(this.base, data, {
            headers: { Authorization: `Bearer ${token}` }
        });
    }

    actualizarEvento(id: number, data: Partial<Evento>): Observable<Evento> {
        const token = localStorage.getItem('token');
        return this.http.put<Evento>(`${this.base}/${id}`, data, {
            headers: { Authorization: `Bearer ${token}` }
        });
    }

    eliminarEvento(id: number): Observable<any> {
        const token = localStorage.getItem('token');
        return this.http.delete(`${this.base}/${id}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
    }

    getImageUrl(path: string): string {
        return this.apiConfig.getImageUrl(path);
    }

    readonly categorias = ['Todos', 'Cultural', 'Deportivo', 'Cívico', 'Comunitario', 'Educativo', 'General'];
}
