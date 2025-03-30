<template>
  <div class="container mt-5">
    <!-- Breadcrumbs mejorados -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4 custom-breadcrumb"></b-breadcrumb>

    <!-- Encabezado con animación -->
    <div class="d-flex justify-content-between align-items-center mb-5 header-animate">
      <h2 class="display-5 fw-bold text-gradient">Explorar Categorías</h2>
      <b-badge variant="primary" pill class="badge-pulse">{{ totalCategorias }} categorías</b-badge>
    </div>

    <!-- Estado de carga mejorado -->
    <div v-if="cargando" class="text-center py-5 loading-wrapper">
      <div class="spinner-grow text-primary spinner" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-3 text-muted fade-in">Cargando categorías...</p>
    </div>

    <!-- Error con mejor diseño -->
    <div v-else-if="error" class="alert alert-danger error-card">
      <div class="d-flex align-items-center">
        <i class="fas fa-exclamation-circle me-3"></i>
        <div>
          <h5 class="alert-heading">Error al cargar</h5>
          <p class="mb-0">{{ error }}</p>
        </div>
      </div>
      <div class="mt-3 text-center">
        <b-button @click="recargarDatos" variant="outline-danger" class="btn-retry">
          <i class="fas fa-sync me-2"></i> Reintentar
        </b-button>
      </div>
    </div>

    <!-- Listado de categorías con mejor diseño -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 category-grid">
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
          class="text-decoration-none card-link"
        >
          <b-card
            class="h-100 category-card"
            :img-src="categoria.imagen_url || placeholderImage"
            img-top
            img-alt="Imagen de categoría"
          >
            <template #header>
              <h5 class="mb-0 text-center card-title">{{ categoria.nombre }}</h5>
            </template>

            <b-card-body class="text-center card-body">
              <p class="text-muted small card-description">{{ categoria.descripcion }}</p>
              <b-badge variant="success" pill class="product-count">
                {{ categoria.conteoProductos }} productos
              </b-badge>
            </b-card-body>

            <template #footer>
              <small class="text-muted card-footer">
                <i class="far fa-clock me-1"></i>
                Actualizado: {{ formatFecha(categoria.updated_at) }}
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
/* Variables de color */
:root {
  --primary-color: #4361ee;
  --secondary-color: #3f37c9;
  --accent-color: #4895ef;
  --light-color: #f8f9fa;
  --dark-color: #212529;
  --success-color: #4cc9f0;
  --danger-color: #f72585;
}

/* Estilos generales */
.container {
  max-width: 1200px;
}

/* Breadcrumbs personalizados */
.custom-breadcrumb {
  background-color: transparent;
  padding: 0;
}

.custom-breadcrumb .breadcrumb-item a {
  color: var(--primary-color);
  text-decoration: none;
  transition: color 0.3s;
}

.custom-breadcrumb .breadcrumb-item a:hover {
  color: var(--secondary-color);
  text-decoration: underline;
}

/* Encabezado con animación */
.header-animate {
  animation: fadeInDown 0.6s ease-out;
}

.text-gradient {
  background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: inline-block;
}

.badge-pulse {
  animation: pulse 2s infinite;
}

/* Tarjetas de categoría */
.category-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: white;
}

.category-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.category-card:hover .card-img-top {
  transform: scale(1.05);
}

.card-title {
  color: var(--dark-color);
  font-weight: 600;
  transition: color 0.3s;
}

.category-card:hover .card-title {
  color: var(--primary-color);
}

.card-description {
  min-height: 40px;
}

.product-count {
  font-size: 0.85rem;
  padding: 0.35em 0.65em;
  background-color: var(--success-color);
}

.card-footer {
  background-color: rgba(248, 249, 250, 0.7);
  border-top: 1px solid rgba(0, 0, 0, 0.03);
}

/* Efecto de carga */
.loading-wrapper {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.spinner {
  width: 4rem;
  height: 4rem;
  opacity: 0;
  animation: fadeIn 0.5s ease-out forwards, spin 1.5s linear infinite;
}

.fade-in {
  animation: fadeIn 1s ease-out;
}

/* Tarjeta de error */
.error-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(247, 37, 133, 0.15);
  background-color: #fff5f7;
  color: #721c24;
  padding: 1.5rem;
}

.btn-retry {
  border-radius: 50px;
  padding: 0.375rem 1.25rem;
  transition: all 0.3s;
}

.btn-retry:hover {
  background-color: var(--danger-color);
  color: white;
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(67, 97, 238, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(67, 97, 238, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(67, 97, 238, 0);
  }
}

/* Grid de categorías */
.category-grid {
  perspective: 1000px;
}

.card-link {
  display: block;
  transition: transform 0.3s;
}

/* Responsive */
@media (max-width: 768px) {
  .header-animate {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .category-card:hover {
    transform: translateY(-5px);
  }
}
</style>