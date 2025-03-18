<template>
    <div class="container mt-5">
      <h2 class="mb-4">Explorar Categorías</h2>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div 
          class="col" 
          v-for="categoria in categorias" 
          :key="categoria.id"
          @click="verProductosCategoria(categoria.nombre)"
        >
          <div class="card h-100 shadow-hover cursor-pointer">
            <div class="card-body text-center">
              <h3 class="card-title">{{ categoria.nombre }}</h3>
              <small class="text-muted">{{ categoria.productos }} productos disponibles</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CategoriasView',
    data() {
      return {
        categorias: [
          { id: 1, nombre: 'Electrónica', productos: 45 },
          { id: 2, nombre: 'Hogar', productos: 32 },
          { id: 3, nombre: 'Moda', productos: 78 },
          { id: 4, nombre: 'Deportes', productos: 56 },
          { id: 5, nombre: 'Juguetes', productos: 23 },
          { id: 6, nombre: 'Libros', productos: 89 },
          { id: 7, nombre: 'Belleza', productos: 67 },
          { id: 8, nombre: 'Automóviles', productos: 12 }
        ]
      };
    },
    methods: {
      verProductosCategoria(categoria) {
        this.$router.push({ 
          name: 'Productos', 
          query: { categoria: categoria.toLowerCase() } 
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .cursor-pointer {
    cursor: pointer;
    transition: transform 0.2s;
  }
  
  .shadow-hover:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  </style>