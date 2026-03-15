import { Pipe, PipeTransform, ChangeDetectorRef, OnDestroy, NgZone } from '@angular/core';

@Pipe({
    name: 'tiempoRelativo',
    standalone: true,
    pure: false // Para que se actualice automáticamente sin recargar
})
export class TiempoRelativoPipe implements PipeTransform, OnDestroy {
    private timer: any;
    private lastValue: string | Date | null | undefined;
    private lastResult: string = '';

    constructor(private cd: ChangeDetectorRef, private zone: NgZone) { }

    transform(value: string | Date | null | undefined): string {
        if (!value) return '';

        this.lastValue = value;

        // Configurar el timer solo una vez por instancia de pipe
        if (!this.timer) {
            this.zone.runOutsideAngular(() => {
                this.timer = setInterval(() => {
                    this.zone.run(() => this.cd.markForCheck());
                }, 60000); // Actualizar cada minuto exacto
            });
        }

        // Asegurarse de que las fechas string del backend (UTC) se parseen correctamente
        let fecha: Date;
        if (typeof value === 'string') {
            // Si la fecha terminaba en hora pero sin zona, le agregamos 'Z' para forzar UTC
            const v = value.endsWith('Z') || value.includes('+') ? value : value + 'Z';
            fecha = new Date(v);
        } else {
            fecha = value;
        }

        const ahora = new Date();
        const diffMs = ahora.getTime() - fecha.getTime();

        // Si el resultado es negativo por desfases pequeños de reloj, mostrar "hace un momento"
        if (diffMs < 0) return 'hace un momento';

        const diffSeg = Math.floor(diffMs / 1000);
        const diffMin = Math.floor(diffSeg / 60);
        const diffHoras = Math.floor(diffMin / 60);
        const diffDias = Math.floor(diffHoras / 24);
        const diffSemanas = Math.floor(diffDias / 7);
        const diffMeses = Math.floor(diffDias / 30);

        let result = '';
        if (diffSeg < 60) result = 'hace un momento';
        else if (diffMin < 60) result = `hace ${diffMin} min`;
        else if (diffHoras < 24) result = diffHoras === 1 ? 'hace 1 hora' : `hace ${diffHoras} horas`;
        else if (diffDias < 7) result = diffDias === 1 ? 'hace 1 día' : `hace ${diffDias} días`;
        else if (diffSemanas < 4) result = diffSemanas === 1 ? 'hace 1 semana' : `hace ${diffSemanas} semanas`;
        else if (diffMeses < 12) result = diffMeses === 1 ? 'hace 1 mes' : `hace ${diffMeses} meses`;
        else result = `hace ${Math.floor(diffMeses / 12)} año(s)`;

        this.lastResult = result;
        return result;
    }

    ngOnDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}
