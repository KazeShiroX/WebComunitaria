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

  getNoticiasPaginadas(pagina: number, itemsPorPagina: number, categoria?: string, busqueda?: string): Observable<PaginacionResult<Noticia>> {
    let params = new HttpParams()
      .set('pagina', pagina.toString())
      .set('items_por_pagina', itemsPorPagina.toString());

    if (categoria && categoria !== 'Todos') {
      params = params.set('categoria', categoria);
    }

    if (busqueda && busqueda.trim()) {
      params = params.set('busqueda', busqueda.trim());
    }

    return this.http.get<any>(this.baseUrl, { params }).pipe(
      map(response => {
        const noticiasApi = response.items.map((item: any) => ({
          ...item,
          fecha: new Date(item.fecha),
          autor: item.autor_nombre
        }));

        // Mock noticia Posada
        const noticiaPosada: Noticia = {
            id: 9999,
            titulo: 'Posada Navideña en Facultad de Agronomía Juan José Ríos',
            descripcion: 'Celebración navideña para niños de la "escuelita" con diferentes actividades y regalos.',
            contenido: 'Se realizó una emotiva posada navideña para los niños de la "escuelita" en las instalaciones de la Facultad de Agronomía Juan José Ríos. Durante el evento, se llevaron a cabo diversas actividades recreativas y juegos para la diversión de los pequeños. El momento más esperado fue la entrega de regalos, donde cada niño recibió un presente navideño, llenando de alegría y sonrisas el lugar. Fue una jornada llena de espíritu navideño y convivencia comunitaria.',
            fecha: new Date(),
            autor: 'Administrador',
            categoria: 'Comunidad',
            imagen: 'images/posada_1.jpg'
        };

        // Add to beginning if searching 'Todos' or 'Comunidad' or empty search
        let items = noticiasApi;
        if ((!categoria || categoria === 'Todos' || categoria === 'Comunidad') && (!busqueda || busqueda.trim() === '')) {
             items = [noticiaPosada, ...noticiasApi];
        }

        return {
          items: items,
          totalItems: response.total_items + 1, // Add 1 for the mock item
          totalPaginas: response.total_paginas, // Keep same for now or calc properly if needed
          paginaActual: response.pagina_actual,
          itemsPorPagina: response.items_por_pagina
        };
      }),
      tap(result => this.noticiasCache.set(result.items)),
      catchError(error => {
        console.error('Error al obtener noticias:', error);
        
        // Fallback with mock data if API fails
        const noticiaPosada: Noticia = {
            id: 9999,
            titulo: 'Posada Navideña en Facultad de Agronomía Juan José Ríos',
            descripcion: 'Celebración navideña para niños de la "escuelita" con diferentes actividades y regalos.',
            contenido: 'Se realizó una emotiva posada navideña para los niños de la "escuelita" en las instalaciones de la Facultad de Agronomía Juan José Ríos. Durante el evento, se llevaron a cabo diversas actividades recreativas y juegos para la diversión de los pequeños. El momento más esperado fue la entrega de regalos, donde cada niño recibió un presente navideño, llenando de alegría y sonrisas el lugar. Fue una jornada llena de espíritu navideño y convivencia comunitaria.',
            fecha: new Date(),
            autor: 'Administrador',
            categoria: 'Comunidad',
            imagen: 'images/posada_1.jpg'
        };

        return of({
          items: [noticiaPosada],
          totalItems: 1,
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
