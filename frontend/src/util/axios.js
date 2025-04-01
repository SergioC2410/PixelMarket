import axios from 'axios';
import store from '@/store';
import router from '@/router';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 30000,  // Aumentado para operaciones pesadas
  withCredentials: true,  // Para manejar cookies si las usas
});

// Interceptor de Request mejorado
axiosInstance.interceptors.request.use(config => {
  const tokenSources = [
    store.state.token,
    localStorage.getItem('access_token'),
    sessionStorage.getItem('temp_token')
  ];
  const token = tokenSources.find(t => t);
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Auto-configuración para FormData
  if (config.data instanceof FormData) {
    Object.assign(config.headers, {
      'Content-Type': 'multipart/form-data',
      'X-Requested-With': 'XMLHttpRequest'
    });
  }

  return config;
});

// Interceptor de Response profesional
axiosInstance.interceptors.response.use(
  response => {
    // Estandarización de respuestas exitosas
    return {
      data: response.data,
      status: response.status,
      headers: response.headers
    };
  },
  error => {
    const { response } = error;
    const errorData = {
      code: response?.status || 500,
      message: response?.data?.detail || 'Error de conexión',
      details: response?.data || {}
    };

    // Manejo avanzado de errores
    switch (errorData.code) {
      case 401:
        store.dispatch('logout');
        router.push({ name: 'login', query: { redirect: router.currentRoute.path } });
        break;
      case 403:
        router.push({ name: 'forbidden' });
        break;
      case 429:
        console.warn('Demasiadas solicitudes - Rate limiting');
        break;
    }

    return Promise.reject(new Error(JSON.stringify(errorData)));
  }
);

export default axiosInstance;