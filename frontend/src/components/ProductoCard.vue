<template>
    <div class="card">
      <img :src="producto.imagen" class="card-img-top" alt="Producto">
      <div class="card-body">
        <h5 class="card-title">{{ producto.nombre }}</h5>
        <p class="card-text">{{ producto.descripcion }}</p>
        <p class="card-text"><strong>Precio:</strong> ${{ producto.precio }}</p>
        <button @click="agregarAlCarrito" class="btn btn-primary">Agregar al carrito</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProductoCard',
    props: {
      producto: {
        type: Object,
        required: true
      }
    },
    methods: {
      agregarAlCarrito() {
        // Lógica para agregar al carrito (usar Vuex)
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos específicos para la tarjeta de producto */
  </style>