<template>
  <div class="container mt-5">
    <h2 class="mb-4">Explorar Categorías</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div 
        class="col" 
        v-for="categoria in categorias" 
        :key="categoria.id"
      >
        <router-link 
          :to="{ name: 'Productos', query: { categoria: categoria.nombre.toLowerCase() } }"
          class="text-decoration-none"
        >
          <div class="card h-100 shadow-hover cursor-pointer">
            <div class="card-body text-center">
              <h3 class="card-title">{{ categoria.nombre }}</h3>
              <small class="text-muted">{{ categoria.productos }} productos disponibles</small>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'CategoriasView',
  computed: {
    ...mapGetters(['categorias']) // Acceder a las categorías desde Vuex
  },
  methods: {
    ...mapActions(['cargarCategorias']) // Llamar la acción de Vuex
  },
  mounted() {
    this.cargarCategorias(); // Cargar las categorías al montar el componente
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

.text-decoration-none {
  text-decoration: none;
  color: inherit;
}
</style>
