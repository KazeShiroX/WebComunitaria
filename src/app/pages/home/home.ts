import { Component, inject, signal, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NoticiasService } from '../../services/noticias.service';
import { ComentariosService, Comentario } from '../../services/comentarios.service';
import { AuthService } from '../../services/auth.service';
import { ApiConfig } from '../../services/api-config.service';
import { TiempoRelativoPipe } from '../../pipes/tiempo-relativo.pipe';
import { PaginacionResult, Noticia } from '../../models/noticia.model';

@Component({
  selector: 'app-home',
  imports: [DatePipe, FormsModule, TiempoRelativoPipe],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  private noticiasService = inject(NoticiasService);
  private comentariosService = inject(ComentariosService);
  private apiConfig = inject(ApiConfig);
  authService = inject(AuthService);
  private router = inject(Router);

  categorias = this.noticiasService.getCategorias();
  categoriaActiva = signal<string>('Todos');
  paginaActual = signal<number>(1);
  terminoBusqueda = signal<string>('');
  itemsPorPagina = 4;

  noticiasPaginadas = signal<PaginacionResult<Noticia>>({
    items: [],
    totalItems: 0,
    totalPaginas: 1,
    paginaActual: 1,
    itemsPorPagina: this.itemsPorPagina
  });

  loading = signal<boolean>(false);

  // Modal de detalle
  showModal = signal<boolean>(false);
  noticiaSeleccionada = signal<Noticia | null>(null);

  // Comentarios con paginación
  comentarios = signal<Comentario[]>([]);
  nuevoComentario = signal<string>('');
  enviandoComentario = signal<boolean>(false);
  paginaComentarios = signal<number>(1);
  totalPaginasComentarios = signal<number>(1);
  totalComentarios = signal<number>(0);
  readonly COMENTARIOS_POR_PAGINA = 5;

  // Reacciones
  reaccionesConteo = signal<{ like: number; love: number; wow: number; sad: number; angry: number }>(
    { like: 0, love: 0, wow: 0, sad: 0, angry: 0 }
  );
  miReaccion = signal<string | null>(null);

  readonly emojis = [
    { tipo: 'like', emoji: '👍', label: 'Me gusta' },
    { tipo: 'love', emoji: '❤️', label: 'Me encanta' },
    { tipo: 'wow', emoji: '😮', label: 'Sorprendido' },
    { tipo: 'sad', emoji: '😢', label: 'Triste' },
    { tipo: 'angry', emoji: '😡', label: 'Enojado' }
  ];

  ngOnInit() {
    this.cargarNoticias();
  }

  getImageUrl(path: string | undefined): string {
    if (!path) return '';
    return this.noticiasService.getImageUrl(path);
  }

  getAvatarUrl(path: string | undefined | null): string {
    if (!path) return '';
    return this.apiConfig.getImageUrl(path);
  }

  cargarNoticias() {
    this.loading.set(true);
    this.noticiasService.getNoticiasPaginadas(
      this.paginaActual(), this.itemsPorPagina,
      this.categoriaActiva(), this.terminoBusqueda()
    ).subscribe({
      next: (result) => { this.noticiasPaginadas.set(result); this.loading.set(false); },
      error: () => { this.loading.set(false); }
    });
  }

  filtrarPorCategoria(categoria: string) {
    this.categoriaActiva.set(categoria);
    this.paginaActual.set(1);
    this.cargarNoticias();
  }

  irAPagina(pagina: number) {
    if (pagina >= 1 && pagina <= this.noticiasPaginadas().totalPaginas) {
      this.paginaActual.set(pagina);
      this.cargarNoticias();
    }
  }

  private searchTimeout: any;
  buscar(event: Event) {
    const input = event.target as HTMLInputElement;
    this.terminoBusqueda.set(input.value);
    if (this.searchTimeout) clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      this.paginaActual.set(1);
      this.cargarNoticias();
    }, 500);
  }

  getPaginas(): (number | string)[] {
    const total = this.noticiasPaginadas().totalPaginas;
    const actual = this.paginaActual();
    const paginas: (number | string)[] = [];
    if (total <= 7) {
      for (let i = 1; i <= total; i++) paginas.push(i);
    } else {
      paginas.push(1);
      if (actual > 3) paginas.push('...');
      for (let i = Math.max(2, actual - 1); i <= Math.min(total - 1, actual + 1); i++) paginas.push(i);
      if (actual < total - 2) paginas.push('...');
      paginas.push(total);
    }
    return paginas;
  }

  getCategoriaColor(categoria: string): string {
    const colores: { [key: string]: string } = {
      'Noticias Locales': '#2563eb',
      'Deportes': '#dc2626',
      'Cultura': '#7c3aed',
      'Comunidad': '#059669',
      'Brigadistas': '#d97706'
    };
    return colores[categoria] || '#666';
  }

  verNoticia(noticia: Noticia) {
    this.noticiaSeleccionada.set(noticia);
    this.showModal.set(true);
    this.paginaComentarios.set(1);
    this.cargarComentariosYReacciones(noticia.id, 1);
  }

  cerrarModal() {
    this.showModal.set(false);
    this.noticiaSeleccionada.set(null);
    this.comentarios.set([]);
    this.nuevoComentario.set('');
    this.reaccionesConteo.set({ like: 0, love: 0, wow: 0, sad: 0, angry: 0 });
    this.miReaccion.set(null);
  }

  // ── Comentarios con paginación ────────────────────────────────────────────

  cargarComentariosYReacciones(noticiaId: number, pagina = 1) {
    this.comentariosService.getComentarios(noticiaId, pagina, this.COMENTARIOS_POR_PAGINA).subscribe(res => {
      this.comentarios.set(res.items);
      this.totalPaginasComentarios.set(res.total_paginas);
      this.totalComentarios.set(res.total);
      this.paginaComentarios.set(res.pagina_actual);
    });

    this.comentariosService.getReacciones(noticiaId).subscribe(res => {
      this.reaccionesConteo.set(res.conteo);
    });

    if (this.authService.isLoggedIn()) {
      this.comentariosService.getMiReaccion(noticiaId).subscribe(res => {
        this.miReaccion.set(res.tipo);
      });
    }
  }

  cambiarPaginaComentarios(pagina: number) {
    const noticiaId = this.noticiaSeleccionada()?.id;
    if (!noticiaId) return;
    if (pagina < 1 || pagina > this.totalPaginasComentarios()) return;
    this.paginaComentarios.set(pagina);
    this.comentariosService.getComentarios(noticiaId, pagina, this.COMENTARIOS_POR_PAGINA).subscribe(res => {
      this.comentarios.set(res.items);
      this.totalPaginasComentarios.set(res.total_paginas);
    });
  }

  enviarComentario() {
    const texto = this.nuevoComentario().trim();
    const noticiaId = this.noticiaSeleccionada()?.id;
    if (!texto || !noticiaId) return;

    this.enviandoComentario.set(true);
    this.comentariosService.agregarComentario(noticiaId, texto).subscribe(comentario => {
      if (comentario) {
        this.nuevoComentario.set('');
        // Recargar desde la última página para ver el comentario nuevo
        this.comentariosService.getComentarios(noticiaId, 1, this.COMENTARIOS_POR_PAGINA).subscribe(res => {
          const ultima = res.total_paginas;
          this.totalComentarios.set(res.total);
          this.totalPaginasComentarios.set(ultima);
          this.cambiarPaginaComentarios(ultima);
        });
      }
      this.enviandoComentario.set(false);
    });
  }

  eliminarComentario(comentarioId: number) {
    this.comentariosService.eliminarComentario(comentarioId).subscribe(ok => {
      if (ok) {
        const noticiaId = this.noticiaSeleccionada()?.id;
        if (noticiaId) this.cargarComentariosYReacciones(noticiaId, this.paginaComentarios());
      }
    });
  }

  // ── Reacciones ───────────────────────────────────────────────────────────

  reaccionar(tipo: string) {
    const noticiaId = this.noticiaSeleccionada()?.id;
    if (!noticiaId) return;
    const reaccionAnterior = this.miReaccion();

    this.comentariosService.reaccionar(noticiaId, tipo).subscribe(res => {
      if (res === null) return;
      const nuevoTipo = res.tipo ?? null;
      const conteo = { ...this.reaccionesConteo() };
      if (reaccionAnterior && reaccionAnterior in conteo)
        conteo[reaccionAnterior as keyof typeof conteo] = Math.max(0, conteo[reaccionAnterior as keyof typeof conteo] - 1);
      if (nuevoTipo && nuevoTipo in conteo)
        conteo[nuevoTipo as keyof typeof conteo]++;
      this.reaccionesConteo.set(conteo);
      this.miReaccion.set(nuevoTipo);
    });
  }

  getReaccionConteo(tipo: string): number {
    const conteo = this.reaccionesConteo();
    return conteo[tipo as keyof typeof conteo] ?? 0;
  }

  irALogin() {
    this.cerrarModal();
    this.router.navigate(['/login']);
  }

  esPropio(comentario: Comentario): boolean {
    return this.authService.usuario()?.id === comentario.usuario_id;
  }
}
