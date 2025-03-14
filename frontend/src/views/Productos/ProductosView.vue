<template>
    <div class="container mt-5">
      <h2>Catálogo de Productos</h2>
      <div class="row">
        <div class="col-md-4" v-for="producto in productos" :key="producto.id">
          <ProductoCard :producto="producto" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ProductoCard from '@/components/ProductoCard.vue';
  
  export default {
    name: 'ProductosView',
    components: {
      ProductoCard
    },
    data() {
      return {
        productos: []  // Datos de productos (se llenarán con Axios)
      };
    },
    created() {
      // Lógica para cargar productos (usar Axios)
    }
  };
  </script>
  
  <style scoped>
  /* Estilos específicos para la página de productos */
  </style>