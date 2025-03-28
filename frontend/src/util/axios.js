import axios from 'axios';
import store from '@/store';  // Si usas Vuex para manejar tokens/auth

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 15000,
});

// Interceptor para manejar peticiones
axiosInstance.interceptors.request.use(config => {
  // Verifica si existe el store y el token
  if (store.state.token || (store.state.auth && store.state.auth.token)) {
    const token = store.state.token || store.state.auth.token;
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  if (config.data instanceof FormData) {
    config.headers['Content-Type'] = 'multipart/form-data';
  }
  
  return config;
});

// Interceptor para manejar respuestas
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    // Manejo centralizado de errores
    const { response } = error;
    
    if (response) {
      const { status, data } = response;
      const errorMessage = data?.detail || data?.message || 'Error desconocido';
      
      // Manejar errores específicos
      switch (status) {
        case 401:
          console.error('No autorizado - Redirigir a login');
          break;
        case 403:
          console.error('Prohibido - Sin permisos');
          break;
        case 404:
          console.error('Recurso no encontrado');
          break;
        case 500:
          console.error('Error interno del servidor');
          break;
      }
      
      return Promise.reject(new Error(JSON.stringify({
        code: status,
        message: errorMessage,
        details: data
      })));
    }
    
    return Promise.reject(new Error(error.message || 'Unknown error'));
  }
);

export default axiosInstance;