import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

/** Guard para rutas que requieren ser admin */
export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  if (authService.isAdmin()) return true;
  router.navigate(['/login']);
  return false;
};

/** Guard para rutas que solo requieren estar logueado (cualquier rol) */
export const loginGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  if (authService.isLoggedIn()) return true;
  router.navigate(['/login']);
  return false;
};

/** Guard para rutas accesibles por moderador o admin */
export const moderadorGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  if (authService.isPowerUser()) return true;
  router.navigate(['/login']);
  return false;
};
