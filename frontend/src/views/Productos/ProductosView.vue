<template>
  <div class="container mt-5">
    <!-- Breadcrumbs -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4"></b-breadcrumb>

    <!-- Barra de búsqueda y filtros -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Productos {{ categoriaActual ? `- ${categoriaActual}` : '' }}</h2>
      <div>
        <b-form-input
          v-model="busqueda"
          placeholder="Buscar productos..."
          class="me-2"
        ></b-form-input>
        <b-button @click="mostrarFiltros = !mostrarFiltros" variant="outline-secondary">
          <i class="fas fa-filter"></i> Filtros
        </b-button>
      </div>
    </div>

    <!-- Filtros -->
    <b-collapse v-model="mostrarFiltros" class="mb-4">
      <b-row>
        <b-col md="4">
          <b-form-select v-model="filtroPrecio" :options="opcionesPrecio" class="mb-2"></b-form-select>
        </b-col>
        <b-col md="4">
          <b-form-select v-model="filtroOrden" :options="opcionesOrden" class="mb-2"></b-form-select>
        </b-col>
      </b-row>
    </b-collapse>

    <!-- Indicador de carga -->
    <div v-if="$store.state.cargando" class="text-center">
      <b-spinner variant="primary"></b-spinner>
      <p>Cargando productos...</p>
    </div>

    <!-- Lista de productos -->
    <div v-else>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="col" v-for="producto in productosFiltrados" :key="producto.id">
          <ProductoCard :producto="producto" />
        </div>
      </div>

      <!-- Paginación -->
      <b-pagination
        v-if="productosFiltrados.length > 0"
        v-model="paginaActual"
        :total-rows="totalProductos"
        :per-page="productosPorPagina"
        class="mt-4"
      ></b-pagination>

      <!-- Mensaje si no hay productos -->
      <div v-if="productosFiltrados.length === 0" class="alert alert-warning mt-4">
        No hay productos disponibles en esta categoría
      </div>
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
      busqueda: '',
      mostrarFiltros: false,
      filtroPrecio: null,
      filtroOrden: null,
      paginaActual: 1,
      productosPorPagina: 6, // Número de productos por página
      opcionesPrecio: [
        { value: null, text: 'Filtrar por precio' },
        { value: '0-50', text: 'Menos de $50' },
        { value: '50-100', text: '$50 - $100' },
        { value: '100-', text: 'Más de $100' }
      ],
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
    breadcrumbs() {
      return [
        { text: 'Inicio', to: '/' },
        { text: 'Categorías', to: '/categorias' },
        { text: this.categoriaActual || 'Productos', active: true }
      ];
    },
    productosFiltrados() {
      let productos = this.$store.getters.productosFiltrados(this.categoriaActual);

      // Filtrar por búsqueda
      if (this.busqueda) {
        productos = productos.filter(p =>
          p.nombre.toLowerCase().includes(this.busqueda.toLowerCase()) ||
          p.descripcion.toLowerCase().includes(this.busqueda.toLowerCase())
        );
      }

      // Filtrar por precio
      if (this.filtroPrecio) {
        const [min, max] = this.filtroPrecio.split('-');
        productos = productos.filter(p => {
          const precio = p.precio;
          return (!min || precio >= parseFloat(min)) && (!max || precio <= parseFloat(max));
        });
      }

      // Ordenar
      if (this.filtroOrden) {
        const [campo, orden] = this.filtroOrden.split('-');
        productos.sort((a, b) => {
          if (campo === 'precio') {
            return orden === 'asc' ? a.precio - b.precio : b.precio - a.precio;
          } else if (campo === 'nombre') {
            return orden === 'asc' 
              ? a.nombre.localeCompare(b.nombre) 
              : b.nombre.localeCompare(a.nombre);
          }
          return 0;
        });
      }

      // Paginación
      const inicio = (this.paginaActual - 1) * this.productosPorPagina;
      const fin = inicio + this.productosPorPagina;
      return productos.slice(inicio, fin);
    },
    totalProductos() {
      return this.$store.getters.productosFiltrados(this.categoriaActual).length;
    }
  },
  created() {
    this.$store.dispatch('cargarProductos'); // Cargar productos al iniciar la vista
  }
};
</script>

<style scoped>
/* Estilos específicos para la página de productos */
.card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>