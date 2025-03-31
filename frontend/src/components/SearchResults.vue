<template>
  <div class="search-results-container">
    <!-- Breadcrumbs -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4"></b-breadcrumb>

    <!-- Header de resultados -->
    <div class="search-header">
      <h2 class="search-title">
        Resultados para: <span class="search-query">"{{ query }}"</span>
      </h2>
      <p class="results-count">{{ totalProductos }} resultados encontrados</p>
    </div>

    <!-- Filtros -->
    <div class="d-flex justify-content-end mb-4">
      <b-form-select 
        v-model="filtroOrden" 
        :options="opcionesOrden" 
        class="me-2"
        @change="filtrarResultados"
        style="width: 250px;"
      ></b-form-select>
    </div>

    <!-- Indicador de carga -->
    <div v-if="estaCargando" class="text-center">
      <b-spinner variant="primary"></b-spinner>
      <p>Cargando resultados...</p>
    </div>

    <!-- Lista de productos -->
    <div v-else>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="col" v-for="producto in productos" :key="producto.id">
          <ProductoCard 
            :producto="producto" 
            @click="verDetalles(producto.id)" 
          />
        </div>
      </div>

      <!-- Paginación -->
      <b-pagination
        v-if="totalProductos > 0"
        v-model="paginaActual"
        :total-rows="totalProductos"
        :per-page="productosPorPagina"
        class="mt-4"
        @input="filtrarResultados"
      ></b-pagination>

      <!-- Mensaje si no hay productos -->
      <div v-if="totalProductos === 0" class="alert alert-warning mt-4">
        No se encontraron productos para "{{ query }}"
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import ProductoCard from '@/components/ProductoCard.vue';

export default {
  name: 'SearchResults',
  components: { ProductoCard },
  props: {
    query: String
  },
  data() {
    return {
      filtroOrden: null,
      paginaActual: 1,
      productosPorPagina: 6,
      opcionesOrden: [
        { value: null, text: 'Ordenar por' },
        { value: 'precio-asc', text: 'Precio: Menor a Mayor' },
        { value: 'precio-desc', text: 'Precio: Mayor a Menor' },
        { value: 'nombre-asc', text: 'Nombre: A-Z' },
        { value: 'nombre-desc', text: 'Nombre: Z-A' }
      ]
    };
  },
  computed: {
    ...mapState({
      productosBusqueda: state => state.productos,
      estaCargando: state => state.cargando,
      paginacion: state => state.paginacion
    }),
    ...mapGetters(['todosProductos']),

    // Aquí se mapea cada producto para actualizar la URL de la imagen
    productos() {
      return this.productosBusqueda.map(producto => {
        const prod = { ...producto };
        if (prod.imagen && !prod.imagen.startsWith('http')) {
          const baseUrl = process.env.NODE_ENV === 'production'
            ? 'https://tudominio.com/media/'
            : 'http://localhost:8000/media/';
          prod.imagen = baseUrl + prod.imagen;
        }
        return prod;
      });
    },

    totalProductos() {
      return this.paginacion.totalItems || 0;
    },

    breadcrumbs() {
      return [
        { text: 'Inicio', to: '/' },
        { text: 'Búsqueda', active: true }
      ];
    }
  },
  methods: {
    ...mapActions(['cargarProductos']),
    
    async filtrarResultados() {
      const params = {
        search: this.query,
        page: this.paginaActual,
        page_size: this.productosPorPagina
      };
      if (this.filtroOrden) {
        params.ordering = this.obtenerOrdenamiento();
      }
      await this.cargarProductos(params);
    },

    obtenerOrdenamiento() {
      switch (this.filtroOrden) {
        case 'precio-asc': return 'precio';
        case 'precio-desc': return '-precio';
        case 'nombre-asc': return 'nombre';
        case 'nombre-desc': return '-nombre';
        default: return null;
      }
    },

    verDetalles(id) {
      this.$router.push({ name: 'DetalleProducto', params: { id } });
    }
  },
  async created() {
    await this.filtrarResultados();
  },
  watch: {
    query() {
      this.paginaActual = 1;
      this.filtrarResultados();
    }
  }
};
</script>

<style scoped>
.search-results-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  animation: fadeIn 0.5s ease;
}

.search-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.search-title {
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.search-query {
  color: var(--color-primary);
  font-weight: 600;
}

.results-count {
  color: #666;
  font-size: 0.9rem;
}

.alert-warning {
  background-color: #fff3cd;
  border-color: #ffeeba;
  color: #856404;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .search-title {
    font-size: 1.5rem;
  }
}
</style>
