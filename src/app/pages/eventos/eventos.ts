import { Component, inject, signal, OnInit, computed } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { EventosService, Evento } from '../../services/eventos.service';
import { ApiConfig } from '../../services/api-config.service';

@Component({
    selector: 'app-eventos',
    imports: [DatePipe, FormsModule],
    templateUrl: './eventos.html',
    styleUrl: './eventos.css'
})
export class Eventos implements OnInit {
    authService = inject(AuthService);
    private eventosSvc = inject(EventosService);
    private apiConfig = inject(ApiConfig);

    categorias = this.eventosSvc.categorias;
    catActiva = signal('Todos');
    todos = signal<Evento[]>([]);
    loading = signal(true);
    mensaje = signal<{ tipo: 'success' | 'error'; texto: string } | null>(null);

    // ── CALENDARIO ──────────────────────────────────────────────────
    hoy = new Date();
    mesActual = signal(new Date(this.hoy.getFullYear(), this.hoy.getMonth(), 1));

    diasEnMes = computed(() => {
        const m = this.mesActual();
        return new Date(m.getFullYear(), m.getMonth() + 1, 0).getDate();
    });

    primerDiaMes = computed(() => this.mesActual().getDay()); // 0=dom

    diaSeleccionado = signal<number | null>(null);

    diasConEventos = computed(() => {
        const m = this.mesActual();
        const set = new Set<number>();
        for (const e of this.todos()) {
            const d = new Date(e.fecha_evento);
            if (d.getFullYear() === m.getFullYear() && d.getMonth() === m.getMonth()) {
                set.add(d.getDate());
            }
        }
        return set;
    });

    eventosFiltrados = computed(() => {
        let lista = this.todos();
        const cat = this.catActiva();
        const dia = this.diaSeleccionado();
        const mes = this.mesActual();

        if (cat !== 'Todos') lista = lista.filter(e => e.categoria === cat);
        if (dia !== null) {
            lista = lista.filter(e => {
                const d = new Date(e.fecha_evento);
                return d.getDate() === dia && d.getMonth() === mes.getMonth() && d.getFullYear() === mes.getFullYear();
            });
        }
        // Próximos primero (positivo), luego pasados (negativo)
        return [...lista].sort((a, b) => {
            const da = a.dias_restantes, db = b.dias_restantes;
            if (da >= 0 && db >= 0) return da - db;
            if (da < 0 && db < 0) return db - da;
            return da >= 0 ? -1 : 1;
        });
    });

    diasCalendario = computed(() => {
        const blancos = this.primerDiaMes();
        const total = this.diasEnMes();
        return [...Array(blancos).fill(null), ...Array.from({ length: total }, (_, i) => i + 1)];
    });

    // ── FORM ─────────────────────────────────────────────────────────
    showForm = signal(false);
    editingEvento = signal<Evento | null>(null);
    guardando = signal(false);
    uploadingImg = signal(false);

    fTitulo = signal('');
    fDescripcion = signal('');
    fCategoria = signal('General');
    fFechaEvento = signal('');
    fLugar = signal('');
    fImagen = signal('');

    ngOnInit() { this.cargar(); }

    cargar() {
        this.loading.set(true);
        this.eventosSvc.getEventos().subscribe(data => {
            this.todos.set(data);
            this.loading.set(false);
        });
    }

    mesMostrado = computed(() => {
        return this.mesActual().toLocaleString('es-MX', { month: 'long', year: 'numeric' });
    });

    cambiarMes(delta: number) {
        const m = this.mesActual();
        this.mesActual.set(new Date(m.getFullYear(), m.getMonth() + delta, 1));
        this.diaSeleccionado.set(null);
    }

    seleccionarDia(dia: number | null) {
        if (!dia) return;
        this.diaSeleccionado.set(this.diaSeleccionado() === dia ? null : dia);
    }

    esHoy(dia: number): boolean {
        const m = this.mesActual();
        return dia === this.hoy.getDate() &&
            m.getMonth() === this.hoy.getMonth() &&
            m.getFullYear() === this.hoy.getFullYear();
    }

    countdownLabel(dias: number): string {
        if (dias === 0) return '¡Hoy!';
        if (dias === 1) return 'Mañana';
        if (dias === -1) return 'Ayer';
        if (dias > 0) return `Faltan ${dias} días`;
        return `Hace ${Math.abs(dias)} días`;
    }

    countdownClass(dias: number): string {
        if (dias === 0) return 'hoy';
        if (dias === 1) return 'manana';
        if (dias > 0 && dias <= 7) return 'pronto';
        if (dias > 0) return 'futuro';
        return 'pasado';
    }

    getCatColor(cat: string): string {
        const m: Record<string, string> = {
            'Cultural': '#7c3aed', 'Deportivo': '#dc2626', 'Cívico': '#2563eb',
            'Comunitario': '#059669', 'Educativo': '#d97706', 'General': '#6b7280'
        };
        return m[cat] || '#6b7280';
    }

    getImageUrl(path: string) { return this.eventosSvc.getImageUrl(path); }

    openForm(e?: Evento) {
        if (e) {
            this.editingEvento.set(e);
            this.fTitulo.set(e.titulo);
            this.fDescripcion.set(e.descripcion);
            this.fCategoria.set(e.categoria);
            this.fFechaEvento.set(e.fecha_evento.slice(0, 16));
            this.fLugar.set(e.lugar);
            this.fImagen.set(e.imagen);
        } else {
            this.resetForm();
        }
        this.showForm.set(true);
    }

    closeForm() { this.showForm.set(false); this.resetForm(); }

    resetForm() {
        this.editingEvento.set(null);
        this.fTitulo.set(''); this.fDescripcion.set('');
        this.fCategoria.set('General'); this.fFechaEvento.set('');
        this.fLugar.set(''); this.fImagen.set('');
    }

    guardar() {
        if (!this.fTitulo() || !this.fDescripcion() || !this.fFechaEvento()) {
            this.mostrarMsg('error', 'Título, descripción y fecha son obligatorios');
            return;
        }
        this.guardando.set(true);
        const payload = {
            titulo: this.fTitulo(), descripcion: this.fDescripcion(),
            categoria: this.fCategoria(),
            fecha_evento: new Date(this.fFechaEvento()).toISOString(),
            lugar: this.fLugar(), imagen: this.fImagen()
        };

        const obs = this.editingEvento()
            ? this.eventosSvc.actualizarEvento(this.editingEvento()!.id, payload)
            : this.eventosSvc.crearEvento(payload);

        obs.subscribe({
            next: () => {
                this.mostrarMsg('success', this.editingEvento() ? 'Evento actualizado' : 'Evento creado');
                this.closeForm(); this.cargar(); this.guardando.set(false);
            },
            error: () => { this.mostrarMsg('error', 'Error al guardar'); this.guardando.set(false); }
        });
    }

    eliminar(id: number) {
        if (!confirm('¿Eliminar este evento?')) return;
        this.eventosSvc.eliminarEvento(id).subscribe(() => {
            this.mostrarMsg('success', 'Evento eliminado');
            this.cargar();
        });
    }

    onFileSelected(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;
        const file = input.files[0];
        this.uploadingImg.set(true);
        const formData = new FormData();
        formData.append('file', file);
        fetch(`${this.apiConfig.baseUrl}/upload`, {
            method: 'POST', body: formData,
            headers: { Authorization: `Bearer ${this.authService.getToken()}` }
        }).then(r => r.json()).then(d => {
            this.fImagen.set(d.url);
            this.uploadingImg.set(false);
        }).catch(() => { this.mostrarMsg('error', 'Error al subir imagen'); this.uploadingImg.set(false); });
    }

    mostrarMsg(tipo: 'success' | 'error', texto: string) {
        this.mensaje.set({ tipo, texto });
        setTimeout(() => this.mensaje.set(null), 3500);
    }
}
