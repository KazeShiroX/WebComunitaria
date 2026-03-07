import { Component, inject, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { AuthService } from '../../services/auth.service';
import { NoticiasService } from '../../services/noticias.service';
import { ComentariosService, Comentario } from '../../services/comentarios.service';
import { ApiConfig } from '../../services/api-config.service';
import { Noticia } from '../../models/noticia.model';

@Component({
    selector: 'app-moderador',
    imports: [FormsModule, DatePipe],
    templateUrl: './moderador.html',
    styleUrl: './moderador.css',
})
export class Moderador implements OnInit {
    authService = inject(AuthService);
    private noticiasService = inject(NoticiasService);
    private comentariosService = inject(ComentariosService);
    private router = inject(Router);
    private apiConfig = inject(ApiConfig);
    private http = inject(HttpClient);

    noticias = signal<Noticia[]>([]);
    categorias = this.noticiasService.getCategorias();
    tabActivo = signal<'noticias' | 'comentarios'>('noticias');

    // Form de noticia
    showForm = signal(false);
    editingNoticia = signal<Noticia | null>(null);
    loading = signal(false);
    uploadingImage = signal(false);
    titulo = signal('');
    descripcion = signal('');
    contenido = signal('');
    categoria = signal('');
    imagen = signal('');

    // Comentarios recientes para moderar
    comentariosRecientes = signal<(Comentario & { noticia_titulo?: string })[]>([]);
    cargandoComentarios = signal(false);

    mensaje = signal<{ tipo: 'success' | 'error'; texto: string } | null>(null);

    constructor() {
        if (!this.authService.isPowerUser()) {
            this.router.navigate(['/login']);
        }
    }

    ngOnInit() {
        this.cargarNoticias();
    }

    irATab(tab: 'noticias' | 'comentarios') {
        this.tabActivo.set(tab);
        if (tab === 'comentarios' && this.comentariosRecientes().length === 0) {
            this.cargarComentariosRecientes();
        }
    }

    cargarNoticias() {
        this.loading.set(true);
        this.noticiasService.getNoticiasPaginadas(1, 100).subscribe({
            next: r => { this.noticias.set(r.items); this.loading.set(false); },
            error: () => this.loading.set(false)
        });
    }

    cargarComentariosRecientes() {
        this.cargandoComentarios.set(true);
        // Cargamos comentarios de todas las noticias (últimas 5)
        const ultimas = this.noticias().slice(0, 5);
        const promesas = ultimas.map(n =>
            this.comentariosService.getComentarios(n.id, 1, 20).toPromise()
                .then(res => (res?.items ?? []).map(c => ({ ...c, noticia_titulo: n.titulo })))
        );
        Promise.all(promesas).then(grupos => {
            const todos = grupos.flat().sort((a, b) =>
                new Date(b.fecha).getTime() - new Date(a.fecha).getTime()
            );
            this.comentariosRecientes.set(todos);
            this.cargandoComentarios.set(false);
        });
    }

    eliminarComentario(id: number) {
        if (!confirm('¿Eliminar este comentario?')) return;
        this.comentariosService.eliminarComentario(id).subscribe(ok => {
            if (ok) {
                this.comentariosRecientes.update(lista => lista.filter(c => c.id !== id));
                this.mostrarMensaje('success', 'Comentario eliminado');
            } else {
                this.mostrarMensaje('error', 'Error al eliminar el comentario');
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

    closeForm() { this.showForm.set(false); this.resetForm(); }

    resetForm() {
        this.editingNoticia.set(null);
        this.titulo.set(''); this.descripcion.set('');
        this.contenido.set(''); this.categoria.set(''); this.imagen.set('');
    }

    guardarNoticia() {
        if (!this.titulo() || !this.descripcion() || !this.categoria()) {
            this.mostrarMensaje('error', 'Completa todos los campos requeridos');
            return;
        }
        this.loading.set(true);
        const data = {
            titulo: this.titulo(), descripcion: this.descripcion(),
            contenido: this.contenido() || '',
            categoria: this.categoria(),
            imagen: this.imagen() || 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=250&fit=crop',
            fecha: new Date(),
            autor: this.authService.usuario()?.nombre || 'Moderador'
        };

        const obs = this.editingNoticia()
            ? this.noticiasService.actualizarNoticia(this.editingNoticia()!.id, data)
            : this.noticiasService.agregarNoticia(data);

        obs.subscribe({
            next: () => {
                this.mostrarMensaje('success', this.editingNoticia() ? 'Noticia actualizada' : 'Noticia creada');
                this.closeForm();
                this.cargarNoticias();
                this.loading.set(false);
            },
            error: () => { this.mostrarMensaje('error', 'Error al guardar'); this.loading.set(false); }
        });
    }

    getImageUrl(path: string) { return this.noticiasService.getImageUrl(path); }

    getCategoriaColor(c: string): string {
        const m: Record<string, string> = {
            'Noticias Locales': '#2563eb', 'Deportes': '#dc2626',
            'Cultura': '#7c3aed', 'Comunidad': '#059669', 'Brigadistas': '#d97706'
        };
        return m[c] || '#666';
    }

    mostrarMensaje(tipo: 'success' | 'error', texto: string) {
        this.mensaje.set({ tipo, texto });
        setTimeout(() => this.mensaje.set(null), 3500);
    }

    onFileSelected(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;
        const file = input.files[0];
        if (!['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'].includes(file.type)) {
            this.mostrarMensaje('error', 'Solo imágenes PNG, JPG, GIF o WEBP'); return;
        }
        if (file.size > 5 * 1024 * 1024) { this.mostrarMensaje('error', 'Máximo 5MB'); return; }
        this.uploadingImage.set(true);
        const formData = new FormData();
        formData.append('file', file);
        fetch(`${this.apiConfig.baseUrl}/upload`, {
            method: 'POST', body: formData,
            headers: { 'Authorization': `Bearer ${this.authService.getToken()}` }
        }).then(r => r.json()).then(d => {
            this.imagen.set(d.url);
            this.mostrarMensaje('success', 'Imagen subida');
            this.uploadingImage.set(false);
        }).catch(() => { this.mostrarMensaje('error', 'Error al subir'); this.uploadingImage.set(false); });
    }
}
