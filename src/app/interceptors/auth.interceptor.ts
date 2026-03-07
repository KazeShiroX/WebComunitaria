import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();

  // Agregar token si existe
  const clonedReq = token
    ? req.clone({ headers: req.headers.set('Authorization', `Bearer ${token}`) })
    : req;

  return next(clonedReq).pipe(
    catchError((error: HttpErrorResponse) => {
      // Si el servidor responde 401, el token es inválido o expiró → cerrar sesión
      if (error.status === 401 && authService.isLoggedIn()) {
        authService.logout();
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};
