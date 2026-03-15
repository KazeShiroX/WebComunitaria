import { Component, inject, signal, computed, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { NotificacionesService, Notificacion } from '../../services/notificaciones.service';
import { ApiConfig } from '../../services/api-config.service';
import { TiempoRelativoPipe } from '../../pipes/tiempo-relativo.pipe';

@Component({
  selector: 'app-header',
  imports: [RouterLink, RouterLinkActive, TiempoRelativoPipe],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header implements OnInit {
  authService = inject(AuthService);
  notifService = inject(NotificacionesService);
  apiConfig = inject(ApiConfig);
  mobileMenuOpen = signal(false);
  notifOpen = signal(false);

  userInitial = computed(() => {
    const usuario = this.authService.usuario();
    return usuario?.nombre ? usuario.nombre.charAt(0).toUpperCase() : '';
  });

  userAvatar = computed(() => {
    const avatar = this.authService.usuario()?.avatar;
    return avatar ? this.apiConfig.getImageUrl(avatar) : '';
  });

  ngOnInit() {
    // Cargar notificaciones si está logueado
    if (this.authService.isLoggedIn()) {
      this.notifService.cargar();
    }
  }

  toggleMobileMenu() {
    this.mobileMenuOpen.update(v => !v);
  }

  toggleNotif() {
    this.notifOpen.update(v => !v);
    // Cargar fresh al abrir
    if (this.notifOpen()) {
      this.notifService.cargar();
    }
  }

  marcarLeida(notif: Notificacion) {
    if (!notif.leida) {
      this.notifService.marcarLeida(notif.id).subscribe();
    }
  }

  marcarTodas() {
    this.notifService.marcarTodasLeidas().subscribe();
  }

  logout() {
    this.authService.logout();
  }
}
