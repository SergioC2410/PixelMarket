import axiosInstance from '@/util/axios';

export default {
  /**
   * Registra un nuevo usuario
   * @param {Object} userData - { email, password, nombre, ... }
   * @returns {Promise} - Respuesta del servidor
   */
  register(userData) {
    return axiosInstance.post('auth/registro/', userData, {
      headers: {
        'X-CSRF-Protection': 'required'  // Si usas CSRF
      }
    });
  },

  /**
   * Inicia sesión y obtiene tokens
   * @param {Object} credentials - { email, password }
   * @returns {Promise} - Contiene tokens de acceso/refresh
   */
  login(credentials) {
    return axiosInstance.post('auth/login/', credentials);
  },

  /**
   * Cierra la sesión del usuario
   * @returns {Promise}
   */
  logout() {
    return axiosInstance.post('auth/logout/');
  },

  /**
   * Renueva el token de acceso
   * @param {String} refreshToken 
   * @returns {Promise} - Nuevo access token
   */
  refreshToken(refreshToken) {
    return axiosInstance.post('auth/token/refresh/', { refresh: refreshToken });
  }
};