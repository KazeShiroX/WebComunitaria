export interface Noticia {
  id: number;
  titulo: string;
  descripcion: string;
  contenido: string;
  categoria: string;
  imagen: string;
  fecha: Date;
  autor: string;
}

export interface PaginacionResult<T> {
  items: T[];
  totalItems: number;
  totalPaginas: number;
  paginaActual: number;
  itemsPorPagina: number;
}
