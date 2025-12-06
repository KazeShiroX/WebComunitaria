// Environment para producción (Railway)
// Railway inyectará RAILWAY_PUBLIC_BACKEND_URL automáticamente
export const environment = {
    production: true,
    apiUrl: '/api'  // Usa ruta relativa porque el mismo servidor sirve frontend y backend
};
