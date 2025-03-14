<template>
    <div class="container mt-5">
      <h2>Checkout</h2>
      <MetodoPago />
      <button @click="finalizarCompra" class="btn btn-success">Finalizar Compra</button>
    </div>
  </template>
  
  <script>
  import MetodoPago from '@/components/MetodoPago.vue';
  
  export default {
    name: 'CheckoutView',
    components: {
      MetodoPago
    },
    methods: {
      finalizarCompra() {
        // Lógica para finalizar la compra (usar Vuex)
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos específicos para la página de checkout */
  </style>