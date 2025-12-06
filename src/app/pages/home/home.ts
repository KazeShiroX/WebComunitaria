import { Component, inject, signal, computed, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { NoticiasService } from '../../services/noticias.service';
import { PaginacionResult, Noticia } from '../../models/noticia.model';

@Component({
  selector: 'app-home',
  imports: [DatePipe],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  private noticiasService = inject(NoticiasService);

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

  ngOnInit() {
    this.cargarNoticias();
  }

  cargarNoticias() {
    this.loading.set(true);
    this.noticiasService.getNoticiasPaginadas(
      this.paginaActual(),
      this.itemsPorPagina,
      this.categoriaActiva(),
      this.terminoBusqueda()
    ).subscribe({
      next: (result) => {
        this.noticiasPaginadas.set(result);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
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

    // Debounce: esperar 500ms después del último cambio para buscar
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
    }

    this.searchTimeout = setTimeout(() => {
      this.paginaActual.set(1); // Volver a la primera página al buscar
      this.cargarNoticias();
    }, 500);
  }

  getPaginas(): (number | string)[] {
    const total = this.noticiasPaginadas().totalPaginas;
    const actual = this.paginaActual();
    const paginas: (number | string)[] = [];

    if (total <= 7) {
      for (let i = 1; i <= total; i++) {
        paginas.push(i);
      }
    } else {
      paginas.push(1);

      if (actual > 3) {
        paginas.push('...');
      }

      for (let i = Math.max(2, actual - 1); i <= Math.min(total - 1, actual + 1); i++) {
        paginas.push(i);
      }

      if (actual < total - 2) {
        paginas.push('...');
      }

      paginas.push(total);
    }

    return paginas;
  }

  getCategoriaColor(categoria: string): string {
    const colores: { [key: string]: string } = {
      'Noticias Locales': '#2563eb',
      'Deportes': '#dc2626',
      'Cultura': '#7c3aed',
      'Comunidad': '#059669'
    };
    return colores[categoria] || '#666';
  }

  verNoticia(noticia: Noticia) {
    this.noticiaSeleccionada.set(noticia);
    this.showModal.set(true);
  }

  cerrarModal() {
    this.showModal.set(false);
    this.noticiaSeleccionada.set(null);
  }
}
