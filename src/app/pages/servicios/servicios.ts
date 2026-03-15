import { Component } from '@angular/core';

interface ServicioItem {
  nombre: string;
  telefonos: string[];
  tipo: string;
  direccion?: string;
}

interface Categoria {
  nombre: string;
  items: ServicioItem[];
}

@Component({
  selector: 'app-servicios',
  templateUrl: './servicios.html',
  styleUrl: './servicios.css'
})
export class Servicios {
  categorias: Categoria[] = [
    {
      nombre: 'Salud y emergencias médicas',
      items: [
        {
          nombre: 'Cruz Roja Mexicana – Juan José Ríos',
          telefonos: ['687 872 0633', '911'],
          tipo: 'Emergencias / Atención prehospitalaria',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Hospital General – Juan José Ríos',
          telefonos: ['687 872 9145', '01 800 623 2323'],
          tipo: 'Hospital / Urgencias',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Clínica ISSSTE – Juan José Ríos',
          telefonos: ['687 872 2230'],
          tipo: 'Clínica / Atención primaria',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Centro de Salud – Juan José Ríos',
          telefonos: ['687 872 0368'],
          tipo: 'Salud pública / Vacunación',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'IMSS – Juan José Ríos',
          telefonos: ['687 872 1800', '01 800 623 2323'],
          tipo: 'Seguro Social / Urgencias',
          direccion: 'Juan José Ríos, Sinaloa'
        }
      ]
    },
    {
      nombre: 'Seguridad pública y tránsito',
      items: [
        {
          nombre: 'Policía Municipal – Juan José Ríos',
          telefonos: ['687 872 1236', '687 872 1232', '060', '911'],
          tipo: 'Seguridad pública',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Tránsito Municipal – Juan José Ríos',
          telefonos: ['687 872 1818', '687 872 4148'],
          tipo: 'Tránsito / Vialidad',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Denuncias anónimas (línea nacional)',
          telefonos: ['089'],
          tipo: 'Denuncias',
          direccion: ''
        }
      ]
    },
    {
      nombre: 'Protección Civil y Bomberos',
      items: [
        {
          nombre: 'Bomberos – Juan José Ríos',
          telefonos: ['687 872 0422', '911'],
          tipo: 'Bomberos / Rescates',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Protección Civil Municipal – Juan José Ríos',
          telefonos: ['687 178 9001'],
          tipo: 'Protección Civil / Atención a desastres',
          direccion: 'Juan José Ríos, Sinaloa'
        }
      ]
    },
    {
      nombre: 'Servicios Públicos',
      items: [
        {
          nombre: 'Comisión Federal de Electricidad (CFE) – Juan José Ríos',
          telefonos: ['071', '687 872 0539', '687 872 1145'],
          tipo: 'Energía eléctrica / Atención a fallas',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Junta de Agua Potable – Juan José Ríos',
          telefonos: ['073', '687 872 7707'],
          tipo: 'Agua potable / Alcantarillado',
          direccion: 'Juan José Ríos, Sinaloa'
        }
      ]
    },
    {
      nombre: 'Otros servicios relevantes',
      items: [
        {
          nombre: 'Presidencia Municipal – Juan José Ríos',
          telefonos: ['687 871 8713'],
          tipo: 'Atención ciudadana',
          direccion: 'Juan José Ríos, Sinaloa'
        },
        {
          nombre: 'Delegación de la Secretaría de Bienestar – Juan José Ríos',
          telefonos: ['687 872 2230'],
          tipo: 'Programas sociales',
          direccion: 'Juan José Ríos, Sinaloa'
        }
      ]
    }
  ];
}
