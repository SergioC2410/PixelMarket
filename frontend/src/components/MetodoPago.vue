<template>
    <div class="metodo-pago">
      <h3>Método de Pago</h3>
      <select v-model="metodoSeleccionado" class="form-select">
        <option value="transferencia">Transferencia</option>
        <option value="efectivo">Efectivo</option>
        <option value="pago_movil">Pago Móvil</option>
      </select>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MetodoPago',
    data() {
      return {
        metodoSeleccionado: 'transferencia'
      };
    }
  };
  </script>
  
  <style scoped>
  /* Estilos específicos para el componente de pago */
  </style>