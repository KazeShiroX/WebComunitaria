import { Routes } from '@angular/router';
import { authGuard, loginGuard, moderadorGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/landing/landing').then(m => m.Landing)
  },

  {
    path: 'noticias',
    loadComponent: () => import('./pages/home/home').then(m => m.Home)
  },
  {
    path: 'eventos',
    loadComponent: () => import('./pages/eventos/eventos').then(m => m.Eventos)
  },
  {
    path: 'contact',
    loadComponent: () => import('./pages/contact/contact.component').then(m => m.ContactComponent)
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then(m => m.Login)
  },
  {
    path: 'perfil',
    loadComponent: () => import('./pages/perfil/perfil').then(m => m.Perfil),
    canActivate: [loginGuard]
  },
  {
    path: 'moderador',
    loadComponent: () => import('./pages/moderador/moderador').then(m => m.Moderador),
    canActivate: [moderadorGuard]
  },
  {
    path: 'admin',
    loadComponent: () => import('./pages/admin/admin').then(m => m.Admin),
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: ''
  }
];
