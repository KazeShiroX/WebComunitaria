import { Component, inject, signal, OnInit, OnDestroy } from '@angular/core';
import { RouterLink } from '@angular/router';
import { NoticiasService } from '../../services/noticias.service';
import { Noticia } from '../../models/noticia.model';
import { TiempoRelativoPipe } from '../../pipes/tiempo-relativo.pipe';

@Component({
    selector: 'app-landing',
    imports: [RouterLink, TiempoRelativoPipe],
    templateUrl: './landing.html',
    styleUrl: './landing.css'
})
export class Landing implements OnInit, OnDestroy {
    private noticiasService = inject(NoticiasService);

    // Contador para forzar re-evaluación del template (y de los pipes impuros)
    tick = signal(0);
    private timer: any;

    destacadas = signal<Noticia[]>([]);
    recientes = signal<Noticia[]>([]);
    loading = signal(true);

    secciones = [
        {
            icon: 'bi-calendar-event',
            titulo: 'Eventos',
            descripcion: 'Ferias, festivales y actividades culturales de la comunidad.',
            color: '#7c3aed',
            bg: '#f5f3ff'
        },
        {
            icon: 'bi-tools',
            titulo: 'Servicios',
            descripcion: 'Trámites, servicios municipales y atención ciudadana.',
            color: '#059669',
            bg: '#f0fdf4'
        },
        {
            icon: 'bi-shield-fill-check',
            titulo: 'Brigadistas',
            descripcion: 'Protección civil, brigadas y emergencias locales.',
            color: '#d97706',
            bg: '#fffbeb'
        },
        {
            icon: 'bi-people-fill',
            titulo: 'Comunidad',
            descripcion: 'Organizaciones, colonias y participación ciudadana.',
            color: '#2563eb',
            bg: '#eff6ff'
        }
    ];

    ngOnInit() {
        this.noticiasService.getNoticiasPaginadas(1, 7).subscribe(res => {
            const todas = res.items;
            this.destacadas.set(todas.slice(0, 3));
            this.recientes.set(todas.slice(3, 7));
            this.loading.set(false);

            // Iniciar el reloj para forzar detección de cambios cada minuto
            this.timer = setInterval(() => {
                this.tick.update(v => v + 1);
            }, 60000);
        });
    }

    ngOnDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }

    getImageUrl(path: string) {
        return this.noticiasService.getImageUrl(path);
    }

    getCategoriaColor(cat: string): string {
        const m: Record<string, string> = {
            'Noticias Locales': '#2563eb', 'Deportes': '#dc2626',
            'Cultura': '#7c3aed', 'Comunidad': '#059669', 'Brigadistas': '#d97706'
        };
        return m[cat] || '#666';
    }
}
