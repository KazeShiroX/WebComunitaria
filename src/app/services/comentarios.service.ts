import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of, map } from 'rxjs';
import { ApiConfig } from './api-config.service';

export interface Comentario {
    id: number;
    noticia_id: number;
    usuario_id: number;
    usuario_nombre: string;
    usuario_avatar?: string;
    texto: string;
    fecha: string;
}

export interface Reaccion {
    id?: number;
    noticia_id: number;
    usuario_id: number;
    tipo: 'like' | 'love' | 'wow' | 'sad' | 'angry';
}

export interface ReaccionesConteo {
    conteo: { like: number; love: number; wow: number; sad: number; angry: number };
    total: number;
}

@Injectable({
    providedIn: 'root'
})
export class ComentariosService {
    private http = inject(HttpClient);
    private apiConfig = inject(ApiConfig);

    private get baseUrl() {
        return this.apiConfig.baseUrl;
    }

    // ── Comentarios ──────────────────────────────────────────────────────────

    getComentarios(noticiaId: number, pagina = 1, porPagina = 5): Observable<{ items: Comentario[]; total: number; total_paginas: number; pagina_actual: number }> {
        return this.http.get<{ items: Comentario[]; total: number; total_paginas: number; pagina_actual: number }>(
            `${this.baseUrl}/noticias/${noticiaId}/comentarios?pagina=${pagina}&items_por_pagina=${porPagina}`
        ).pipe(catchError(() => of({ items: [], total: 0, total_paginas: 1, pagina_actual: 1 })));
    }

    agregarComentario(noticiaId: number, texto: string): Observable<Comentario | null> {
        return this.http.post<Comentario>(
            `${this.baseUrl}/noticias/${noticiaId}/comentarios`,
            { texto }
        ).pipe(catchError(() => of(null)));
    }

    eliminarComentario(comentarioId: number): Observable<boolean> {
        return this.http.delete(`${this.baseUrl}/comentarios/${comentarioId}`).pipe(
            map(() => true),
            catchError(() => of(false))
        );
    }

    // ── Reacciones ───────────────────────────────────────────────────────────

    getReacciones(noticiaId: number): Observable<ReaccionesConteo> {
        return this.http.get<ReaccionesConteo>(
            `${this.baseUrl}/noticias/${noticiaId}/reacciones`
        ).pipe(catchError(() => of({ conteo: { like: 0, love: 0, wow: 0, sad: 0, angry: 0 }, total: 0 })));
    }

    getMiReaccion(noticiaId: number): Observable<{ tipo: string | null }> {
        return this.http.get<{ tipo: string | null }>(
            `${this.baseUrl}/noticias/${noticiaId}/reacciones/mi-reaccion`
        ).pipe(catchError(() => of({ tipo: null })));
    }

    reaccionar(noticiaId: number, tipo: string): Observable<any> {
        return this.http.post(
            `${this.baseUrl}/noticias/${noticiaId}/reacciones`,
            { tipo }
        ).pipe(catchError(() => of(null)));
    }
}
