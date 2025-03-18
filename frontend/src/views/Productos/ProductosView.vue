<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Productos {{ categoriaActual ? `- ${categoriaActual}` : '' }}</h2>
      <button @click="$router.go(-1)" class="btn btn-outline-secondary">
        Volver a categorías
      </button>
    </div>
    
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="producto in productosFiltrados" :key="producto.id">
        <ProductoCard :producto="producto" />
      </div>
    </div>

    <div v-if="productosFiltrados.length === 0" class="alert alert-warning mt-4">
      No hay productos disponibles en esta categoría
    </div>
  </div>
</template>

<script>
import ProductoCard from '@/components/ProductoCard.vue';

export default {
  name: 'ProductosView',
  components: { ProductoCard },
  data() {
    return {
      categoriaActual: this.$route.query.categoria || '',
      productos: [
        // Ejemplo de productos falsos
        { 
          id: 1, 
          nombre: 'Smartphone X', 
          precio: 599.99, 
          categoria: 'electrónica',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Teléfono inteligente última generación'
        },
        { 
          id: 2, 
          nombre: 'Sofá Moderno', 
          precio: 899.99, 
          categoria: 'hogar',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Sofá de diseño escandinavo'
        },
        // Agregar más productos...
      ]
    };
  },
  computed: {
    productosFiltrados() {
      if (!this.categoriaActual) return this.productos;
      return this.productos.filter(p => 
        p.categoria.toLowerCase() === this.categoriaActual.toLowerCase()
      );
    }
  }
};
</script>
<style scoped>
/* Estilos específicos para la página de productos */
</style>