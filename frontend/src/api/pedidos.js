import axiosInstance from '@/util/axios';

export default {
  /**
   * Crea un nuevo pedido
   * @param {Object} orderData - { items, metodo_entrega, ... }
   * @returns {Promise} - Pedido creado
   */
  createOrder(orderData) {
    return axiosInstance.post('pedidos/crear/', orderData, {
      headers: {
        'Idempotency-Key': generateIdempotencyKey()  // Previene duplicados
      }
    });
  },

  /**
   * Cancela un pedido existente
   * @param {Number} orderId - ID del pedido
   * @returns {Promise}
   */
  cancelOrder(orderId) {
    return axiosInstance.post(`pedidos/${orderId}/cancelar/`);
  },

  /**
   * Obtiene el historial de pedidos
   * @param {Object} params - { page, page_size, estado, ... }
   * @returns {Promise} - Lista paginada de pedidos
   */
  getOrderHistory(params = {}) {
    return axiosInstance.get('pedidos/', { params });
  }
};

// Helper para claves idempotentes
function generateIdempotencyKey() {
  return 'idemp_' + Date.now() + '_' + Math.random().toString(36).substring(2, 11);
}