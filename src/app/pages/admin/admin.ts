import { Component, inject, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { NoticiasService } from '../../services/noticias.service';
import { Noticia } from '../../models/noticia.model';

@Component({
  selector: 'app-admin',
  imports: [FormsModule, DatePipe],
  templateUrl: './admin.html',
  styleUrl: './admin.css',
})
export class Admin implements OnInit {
  authService = inject(AuthService);
  private noticiasService = inject(NoticiasService);
  private router = inject(Router);

  noticias = signal<Noticia[]>([]);
  categorias = this.noticiasService.getCategorias();
  
  showForm = signal(false);
  editingNoticia = signal<Noticia | null>(null);
  loading = signal(false);
  
  // Form fields
  titulo = signal('');
  descripcion = signal('');
  contenido = signal('');
  categoria = signal('');
  imagen = signal('');
  
  mensaje = signal<{tipo: 'success' | 'error', texto: string} | null>(null);

  constructor() {
    // Verificar autenticación
    if (!this.authService.isAdmin()) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit() {
    this.cargarNoticias();
  }

  cargarNoticias() {
    this.loading.set(true);
    this.noticiasService.getNoticiasPaginadas(1, 100).subscribe({
      next: (result) => {
        this.noticias.set(result.items);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.mostrarMensaje('error', 'Error al cargar las noticias');
      }
    });
  }

  openForm(noticia?: Noticia) {
    if (noticia) {
      this.editingNoticia.set(noticia);
      this.titulo.set(noticia.titulo);
      this.descripcion.set(noticia.descripcion);
      this.contenido.set(noticia.contenido);
      this.categoria.set(noticia.categoria);
      this.imagen.set(noticia.imagen);
    } else {
      this.resetForm();
    }
    this.showForm.set(true);
  }

  closeForm() {
    this.showForm.set(false);
    this.resetForm();
  }

  resetForm() {
    this.editingNoticia.set(null);
    this.titulo.set('');
    this.descripcion.set('');
    this.contenido.set('');
    this.categoria.set('');
    this.imagen.set('');
  }

  guardarNoticia() {
    if (!this.titulo() || !this.descripcion() || !this.categoria()) {
      this.mostrarMensaje('error', 'Por favor completa todos los campos requeridos');
      return;
    }

    this.loading.set(true);

    const noticiaData = {
      titulo: this.titulo(),
      descripcion: this.descripcion(),
      contenido: this.contenido() || this.descripcion(),
      categoria: this.categoria(),
      imagen: this.imagen() || 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=250&fit=crop',
      fecha: new Date(),
      autor: this.authService.usuario()?.nombre || 'Administrador'
    };

    if (this.editingNoticia()) {
      this.noticiasService.actualizarNoticia(this.editingNoticia()!.id, noticiaData).subscribe({
        next: () => {
          this.mostrarMensaje('success', 'Noticia actualizada correctamente');
          this.closeForm();
          this.cargarNoticias();
          this.loading.set(false);
        },
        error: () => {
          this.mostrarMensaje('error', 'Error al actualizar la noticia');
          this.loading.set(false);
        }
      });
    } else {
      this.noticiasService.agregarNoticia(noticiaData).subscribe({
        next: () => {
          this.mostrarMensaje('success', 'Noticia creada correctamente');
          this.closeForm();
          this.cargarNoticias();
          this.loading.set(false);
        },
        error: () => {
          this.mostrarMensaje('error', 'Error al crear la noticia');
          this.loading.set(false);
        }
      });
    }
  }

  eliminarNoticia(id: number) {
    if (confirm('¿Estás seguro de que deseas eliminar esta noticia?')) {
      this.loading.set(true);
      this.noticiasService.eliminarNoticia(id).subscribe({
        next: (success) => {
          if (success) {
            this.mostrarMensaje('success', 'Noticia eliminada correctamente');
            this.cargarNoticias();
          } else {
            this.mostrarMensaje('error', 'Error al eliminar la noticia');
          }
          this.loading.set(false);
        },
        error: () => {
          this.mostrarMensaje('error', 'Error al eliminar la noticia');
          this.loading.set(false);
        }
      });
    }
  }

  mostrarMensaje(tipo: 'success' | 'error', texto: string) {
    this.mensaje.set({ tipo, texto });
    setTimeout(() => this.mensaje.set(null), 3000);
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
}