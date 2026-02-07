import { Component, inject, signal, computed } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header {
  authService = inject(AuthService);
  mobileMenuOpen = signal(false);

  userInitial = computed(() => {
    const usuario = this.authService.usuario();
    return usuario?.nombre ? usuario.nombre.charAt(0).toUpperCase() : '';
  });

  toggleMobileMenu() {
    this.mobileMenuOpen.update(v => !v);
  }

  logout() {
    this.authService.logout();
  }
}
