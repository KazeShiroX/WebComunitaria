import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Header } from './components/header/header';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Header],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private authService = inject(AuthService);

  ngOnInit() {
    // Verificar token al iniciar la app: si existe pero es inválido, hace logout automático
    this.authService.verificarToken().subscribe();
  }
}
