<template>
  <div class="container mt-5">
    <!-- Breadcrumbs -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4"></b-breadcrumb>

    <!-- Barra de búsqueda y filtros -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Productos {{ categoriaActual ? `- ${categoriaActual.nombre}` : '' }}</h2>
      <div>
        <b-form-input 
          v-model="busqueda" 
          placeholder="Buscar productos..." 
          class="me-2"
          @input="filtrarProductos"
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
          <b-form-select 
            v-model="filtroPrecio" 
            :options="opcionesPrecio" 
            class="mb-2"
            @change="filtrarProductos"
          ></b-form-select>
        </b-col>
        <b-col md="4">
          <b-form-select 
            v-model="filtroOrden" 
            :options="opcionesOrden" 
            class="mb-2"
            @change="filtrarProductos"
          ></b-form-select>
        </b-col>
        <b-col md="4">
          <b-form-select
            v-model="filtroCategoria"
            :options="opcionesCategoria"
            class="mb-2"
            @change="cambiarCategoria"
          ></b-form-select>
        </b-col>
      </b-row>
    </b-collapse>

    <!-- Indicador de carga -->
    <div v-if="estaCargando" class="text-center">
      <b-spinner variant="primary"></b-spinner>
      <p>Cargando productos...</p>
    </div>

    <!-- Lista de productos -->
    <div v-else>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="col" v-for="producto in productosPaginados" :key="producto.id">
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
        @input="filtrarProductos"
      ></b-pagination>

      <!-- Mensaje si no hay productos -->
      <div v-if="totalProductos === 0" class="alert alert-warning mt-4">
        No se encontraron productos con los filtros aplicados
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import ProductoCard from '@/components/ProductoCard.vue';

export default {
  name: 'ProductosView',
  components: { ProductoCard },
  data() {
    return {
      busqueda: '',
      mostrarFiltros: false,
      filtroPrecio: null,
      filtroOrden: null,
      filtroCategoria: null,
      paginaActual: 1,
      productosPorPagina: 6,
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
      ],
      paramsFiltro: {}
    };
  },
  computed: {
    ...mapGetters(['todosProductos', 'productosDisponibles', 'todasCategorias', 'estaCargando']),
    ...mapState(['error']),

    categoriaActual() {
      if (!this.filtroCategoria) return null;
      return this.todasCategorias.find(c => c.id === this.filtroCategoria);
    },

    opcionesCategoria() {
      return [
        { value: null, text: 'Todas las categorías' },
        ...this.todasCategorias.map(c => ({
          value: c.id,
          text: c.nombre
        }))
      ];
    },

    productosFiltrados() {
      let productos = this.todosProductos;
      
      // Filtro por búsqueda
      if (this.busqueda) {
        const busquedaLower = this.busqueda.toLowerCase();
        productos = productos.filter(p =>
          p.nombre.toLowerCase().includes(busquedaLower) ||
          p.descripcion.toLowerCase().includes(busquedaLower)
        );
      }

      // Filtro por categoría
      if (this.filtroCategoria) {
        productos = productos.filter(p => p.categoria.id === this.filtroCategoria);
      }

      // Filtro por precio
      if (this.filtroPrecio) {
        const [min, max] = this.filtroPrecio.split('-');
        if (min) productos = productos.filter(p => p.precio >= parseFloat(min));
        if (max) productos = productos.filter(p => p.precio <= parseFloat(max));
      }

      return productos;
    },

    productosOrdenados() {
      if (this.filtroOrden === 'precio-asc') {
        return [...this.productosFiltrados].sort((a, b) => a.precio - b.precio);
      } else if (this.filtroOrden === 'precio-desc') {
        return [...this.productosFiltrados].sort((a, b) => b.precio - a.precio);
      } else if (this.filtroOrden === 'nombre-asc') {
        return [...this.productosFiltrados].sort((a, b) => a.nombre.localeCompare(b.nombre));
      } else if (this.filtroOrden === 'nombre-desc') {
        return [...this.productosFiltrados].sort((a, b) => b.nombre.localeCompare(a.nombre));
      }
      return this.productosFiltrados;
    },

    totalProductos() {
      return this.productosOrdenados.length;
    },

    productosPaginados() {
      const inicio = (this.paginaActual - 1) * this.productosPorPagina;
      return this.productosOrdenados.slice(inicio, inicio + this.productosPorPagina);
    },

    breadcrumbs() {
      return [
        { text: 'Inicio', to: '/' },
        { text: 'Productos', active: true }
      ];
    },
  },
  methods: {
    ...mapActions(['cargarProductos', 'cargarCategorias']),

    async filtrarProductos() {
      this.paramsFiltro = {
        search: this.busqueda,
        categoria_id: this.filtroCategoria,
        ordering: this.obtenerOrdenamiento(),
        page: this.paginaActual
      };

      if (this.filtroPrecio) {
        const [min, max] = this.filtroPrecio.split('-');
        if (min) this.paramsFiltro.precio_min = min;
        if (max) this.paramsFiltro.precio_max = max;
      }

      await this.cargarProductos(this.paramsFiltro);
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

    cambiarCategoria() {
      this.paginaActual = 1;
      this.filtrarProductos();
    },

    verDetalles(id) {
      this.$router.push({ name: 'DetalleProducto', params: { id } });
    }
  },
  async created() {
    await this.cargarCategorias();
    await this.filtrarProductos();
    
    // Si viene categoría por URL
    if (this.$route.query.categoria) {
      this.filtroCategoria = parseInt(this.$route.query.categoria);
    }
  },
  watch: {
    '$route.query.categoria'(newVal) {
      if (newVal) {
        this.filtroCategoria = parseInt(newVal);
        this.filtrarProductos();
      }
    }
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.alert-warning {
  background-color: #fff3cd;
  border-color: #ffeeba;
  color: #856404;
}
</style>