import axiosInstance from '@/util/axios';

export default {
  /**
   * Obtiene el perfil completo del usuario
   * @returns {Promise} - Datos del perfil
   */
  getProfile() {
    return axiosInstance.get('usuarios/perfil/');
  },

  /**
   * Actualiza el perfil del usuario
   * @param {Object} profileData - Datos a actualizar
   * @returns {Promise}
   */
  updateProfile(profileData) {
    return axiosInstance.patch('usuarios/perfil/actualizar/', profileData);
  },

  /**
   * Gestiona la ubicación del usuario
   * @param {Object} locationData - { direccion, ciudad, ... }
   * @returns {Promise}
   */
  updateLocation(locationData) {
    return axiosInstance.put('usuarios/ubicacion/', locationData);
  }
};