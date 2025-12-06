import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home').then(m => m.Home)
  },
  {
    path: 'noticias',
    loadComponent: () => import('./pages/home/home').then(m => m.Home)
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then(m => m.Login)
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
