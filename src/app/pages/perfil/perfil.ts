import { Component, inject, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ApiConfig } from '../../services/api-config.service';

@Component({
    selector: 'app-perfil',
    imports: [FormsModule, RouterLink],
    templateUrl: './perfil.html',
    styleUrl: './perfil.css'
})
export class Perfil implements OnInit {
    authService = inject(AuthService);
    private apiConfig = inject(ApiConfig);

    nombre = signal('');
    avatarUrl = signal('');
    uploadingAvatar = signal(false);
    saving = signal(false);
    mensaje = signal<{ tipo: 'success' | 'error'; texto: string } | null>(null);

    ngOnInit() {
        const u = this.authService.usuario();
        if (u) {
            this.nombre.set(u.nombre);
            this.avatarUrl.set(u.avatar ?? '');
        }
    }

    getImageUrl(path: string): string {
        if (!path) return '';
        return this.apiConfig.getImageUrl(path);
    }

    onAvatarSelected(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;

        const file = input.files[0];
        const allowed = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
        if (!allowed.includes(file.type)) {
            this.mostrarMensaje('error', 'Solo imágenes PNG, JPG, GIF o WEBP');
            return;
        }
        if (file.size > 5 * 1024 * 1024) {
            this.mostrarMensaje('error', 'La imagen no puede superar 5MB');
            return;
        }

        this.uploadingAvatar.set(true);
        const formData = new FormData();
        formData.append('file', file);

        fetch(`${this.apiConfig.baseUrl}/upload`, {
            method: 'POST',
            body: formData,
            headers: { 'Authorization': `Bearer ${this.authService.getToken()}` }
        })
            .then(r => r.json())
            .then(data => {
                this.avatarUrl.set(data.url);
                this.mostrarMensaje('success', 'Imagen subida. Guarda los cambios para aplicarla.');
                this.uploadingAvatar.set(false);
            })
            .catch(() => {
                this.mostrarMensaje('error', 'Error al subir la imagen');
                this.uploadingAvatar.set(false);
            });
    }

    guardarCambios() {
        if (!this.nombre().trim()) {
            this.mostrarMensaje('error', 'El nombre no puede estar vacío');
            return;
        }
        this.saving.set(true);
        this.authService.actualizarPerfil(this.nombre().trim(), this.avatarUrl() || undefined)
            .subscribe(result => {
                this.mostrarMensaje(result.success ? 'success' : 'error', result.message);
                this.saving.set(false);
            });
    }

    mostrarMensaje(tipo: 'success' | 'error', texto: string) {
        this.mensaje.set({ tipo, texto });
        setTimeout(() => this.mensaje.set(null), 4000);
    }
}
