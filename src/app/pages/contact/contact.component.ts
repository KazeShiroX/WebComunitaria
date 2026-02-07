import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface TeamMember {
    name: string;
    role: string;
    image?: string;
}

@Component({
    selector: 'app-contact',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './contact.component.html',
    styleUrls: ['./contact.component.css']
})
export class ContactComponent {
    brigadistas: TeamMember[] = [
        { name: 'Ruiz Rosas Kevin', role: 'Brigadista' },
        { name: 'Gutierrez Ramirez Jose Manuel', role: 'Brigadista' },
        { name: 'Cota Buelna Ruben', role: 'Brigadista' }
    ];

    advisor: TeamMember = {
        name: 'Alvaro Eleazar Alvarez',
        role: 'Asesor'
    };
}
