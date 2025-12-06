import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, tap, map, catchError, of } from 'rxjs';
import { Noticia, PaginacionResult } from '../models/noticia.model';
import { ApiConfig } from './api-config.service';

@Injectable({
  providedIn: 'root'
})
export class NoticiasService {
  private http = inject(HttpClient);
  private apiConfig = inject(ApiConfig);
  
  private baseUrl = `${this.apiConfig.baseUrl}/noticias`;
  
  private categorias = signal<string[]>(['Todos', 'Noticias Locales', 'Deportes', 'Cultura', 'Comunidad']);
  private noticiasCache = signal<Noticia[]>([]);

  getCategorias() {
    return this.categorias;
  }

  getNoticias() {
    return this.noticiasCache;
  }

  getNoticiasPaginadas(pagina: number, itemsPorPagina: number, categoria?: string): Observable<PaginacionResult<Noticia>> {
    let params = new HttpParams()
      .set('pagina', pagina.toString())
      .set('items_por_pagina', itemsPorPagina.toString());
    
    if (categoria && categoria !== 'Todos') {
      params = params.set('categoria', categoria);
    }

    return this.http.get<any>(this.baseUrl, { params }).pipe(
      map(response => ({
        items: response.items.map((item: any) => ({
          ...item,
          fecha: new Date(item.fecha),
          autor: item.autor_nombre
        })),
        totalItems: response.total_items,
        totalPaginas: response.total_paginas,
        paginaActual: response.pagina_actual,
        itemsPorPagina: response.items_por_pagina
      })),
      tap(result => this.noticiasCache.set(result.items)),
      catchError(error => {
        console.error('Error al obtener noticias:', error);
        return of({
          items: [],
          totalItems: 0,
          totalPaginas: 1,
          paginaActual: 1,
          itemsPorPagina
        });
      })
    );
  }

  getNoticiaPorId(id: number): Observable<Noticia | undefined> {
    return this.http.get<any>(`${this.baseUrl}/${id}`).pipe(
      map(item => ({
        ...item,
        fecha: new Date(item.fecha),
        autor: item.autor_nombre
      })),
      catchError(() => of(undefined))
    );
  }

  agregarNoticia(noticia: Omit<Noticia, 'id'>): Observable<Noticia> {
    return this.http.post<any>(this.baseUrl, {
      titulo: noticia.titulo,
      descripcion: noticia.descripcion,
      contenido: noticia.contenido,
      categoria: noticia.categoria,
      imagen: noticia.imagen
    }).pipe(
      map(item => ({
        ...item,
        fecha: new Date(item.fecha),
        autor: item.autor_nombre
      }))
    );
  }

  actualizarNoticia(id: number, noticia: Partial<Noticia>): Observable<Noticia> {
    return this.http.put<any>(`${this.baseUrl}/${id}`, {
      titulo: noticia.titulo,
      descripcion: noticia.descripcion,
      contenido: noticia.contenido,
      categoria: noticia.categoria,
      imagen: noticia.imagen
    }).pipe(
      map(item => ({
        ...item,
        fecha: new Date(item.fecha),
        autor: item.autor_nombre
      }))
    );
  }

  eliminarNoticia(id: number): Observable<boolean> {
    return this.http.delete<any>(`${this.baseUrl}/${id}`).pipe(
      map(() => true),
      catchError(() => of(false))
    );
  }

  buscarNoticias(termino: string): Observable<Noticia[]> {
    const params = new HttpParams().set('busqueda', termino);
    return this.http.get<any>(this.baseUrl, { params }).pipe(
      map(response => response.items.map((item: any) => ({
        ...item,
        fecha: new Date(item.fecha),
        autor: item.autor_nombre
      }))),
      catchError(() => of([]))
    );
  }
}
