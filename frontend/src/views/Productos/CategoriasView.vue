<template>
  <div class="container mt-5">
    <!-- Breadcrumbs -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4"></b-breadcrumb>

    <!-- Encabezado -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Explorar Categorías</h2>
      <b-badge variant="primary" pill>{{ totalCategorias }} categorías</b-badge>
    </div>

    <!-- Estado de carga -->
    <div v-if="cargando" class="text-center py-5">
      <b-spinner variant="primary" label="Cargando..."></b-spinner>
      <p>Cargando categorías...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
      <b-button @click="recargarDatos" variant="outline-danger" class="ms-3">
        <i class="fas fa-sync"></i> Reintentar
      </b-button>
    </div>

    <!-- Listado de categorías -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div 
        v-for="categoria in categoriasConConteo" 
        :key="categoria.id" 
        class="col"
      >
        <router-link 
          :to="{ 
            name: 'Productos', 
            query: { categoria: categoria.id } 
          }" 
          class="text-decoration-none"
        >
          <b-card
            class="h-100 hover-effect"
            :img-src="categoria.imagen_url || placeholderImage"
            img-top
          >
            <template #header>
              <h5 class="mb-0 text-center">{{ categoria.nombre }}</h5>
            </template>

            <b-card-body class="text-center">
              <p class="text-muted small">{{ categoria.descripcion }}</p>
              <b-badge variant="success" pill>
                {{ categoria.conteoProductos }} productos
              </b-badge>
            </b-card-body>

            <template #footer>
              <small class="text-muted">
                Última actualización: {{ formatFecha(categoria.updated_at) }}
              </small>
            </template>
          </b-card>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'

export default {
  name: 'CategoriasView',
  data() {
    return {
      placeholderImage: 'https://via.placeholder.com/400x200.png?text=Categoría+Sin+Imagen',
      breadcrumbs: [
        { text: 'Inicio', to: '/' },
        { text: 'Categorías', active: true }
      ]
    }
  },
  computed: {
    ...mapGetters(['todasCategorias', 'productosPorCategoria']),
    ...mapState(['estaCargando', 'error']),
    
    cargando() {
      return this.estaCargando
    },
    
    totalCategorias() {
      return this.todasCategorias.length
    },
    
    categoriasConConteo() {
      return this.todasCategorias.map(categoria => ({
        ...categoria,
        conteoProductos: this.productosPorCategoria(categoria.id).length,
        updated_at: categoria.fecha_actualizacion || new Date().toISOString()
      }))
    }
  },
  methods: {
    ...mapActions(['cargarCategorias', 'cargarProductos']),
    
    formatFecha(fecha) {
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },
    
    async recargarDatos() {
      try {
        await Promise.all([
          this.cargarCategorias(),
          this.cargarProductos()
        ])
      } catch (error) {
        console.error('Error recargando datos:', error)
      }
    }
  },
  async mounted() {
    if (this.todasCategorias.length === 0) {
      await this.recargarDatos()
    }
  }
}
</script>

<style scoped>
.hover-effect {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.text-decoration-none {
  color: inherit;
}

.text-decoration-none:hover {
  color: inherit;
  text-decoration: none;
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}
</style>