import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  private authService = inject(AuthService);
  private router = inject(Router);

  isLoginMode = signal(true);
  email = signal('');
  password = signal('');
  nombre = signal('');
  error = signal('');
  loading = signal(false);

  toggleMode() {
    this.isLoginMode.update(v => !v);
    this.error.set('');
  }

  onSubmit() {
    this.error.set('');
    this.loading.set(true);

    if (this.isLoginMode()) {
      this.authService.login({
        email: this.email(),
        password: this.password()
      }).subscribe({
        next: (result) => {
          if (result.success) {
            this.router.navigate(['/']);
          } else {
            this.error.set(result.message);
          }
          this.loading.set(false);
        },
        error: () => {
          this.error.set('Error de conexión');
          this.loading.set(false);
        }
      });
    } else {
      this.authService.register({
        nombre: this.nombre(),
        email: this.email(),
        password: this.password()
      }).subscribe({
        next: (result) => {
          if (result.success) {
            this.router.navigate(['/admin']);
          } else {
            this.error.set(result.message);
          }
          this.loading.set(false);
        },
        error: () => {
          this.error.set('Error de conexión');
          this.loading.set(false);
        }
      });
    }
  }
}
