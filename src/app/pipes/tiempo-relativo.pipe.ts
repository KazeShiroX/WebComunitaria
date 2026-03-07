import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'tiempoRelativo',
    standalone: true
})
export class TiempoRelativoPipe implements PipeTransform {
    transform(value: string | Date | null | undefined): string {
        if (!value) return '';

        const fecha = typeof value === 'string' ? new Date(value) : value;
        const ahora = new Date();
        const diffMs = ahora.getTime() - fecha.getTime();
        const diffSeg = Math.floor(diffMs / 1000);
        const diffMin = Math.floor(diffSeg / 60);
        const diffHoras = Math.floor(diffMin / 60);
        const diffDias = Math.floor(diffHoras / 24);
        const diffSemanas = Math.floor(diffDias / 7);
        const diffMeses = Math.floor(diffDias / 30);

        if (diffSeg < 60) return 'hace un momento';
        if (diffMin < 60) return `hace ${diffMin} min`;
        if (diffHoras < 24) return diffHoras === 1 ? 'hace 1 hora' : `hace ${diffHoras} horas`;
        if (diffDias < 7) return diffDias === 1 ? 'hace 1 día' : `hace ${diffDias} días`;
        if (diffSemanas < 4) return diffSemanas === 1 ? 'hace 1 semana' : `hace ${diffSemanas} semanas`;
        if (diffMeses < 12) return diffMeses === 1 ? 'hace 1 mes' : `hace ${diffMeses} meses`;
        return `hace ${Math.floor(diffMeses / 12)} año(s)`;
    }
}
