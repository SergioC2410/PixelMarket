<template>
  <div class="home-view">
    <main class="main-content">
      <!-- Sección de marcas -->
      <BrandsSection :brands="brands" />
      
      <!-- Sección de descuentos -->
      <ProductsSection 
        v-if="productosConDescuento.length > 0"
        title="Descuentos del Día"
        :products="productosConDescuento"
        show-discount
      />
      
      <!-- Carrusel de categorías -->
      <CategoriesSection 
        v-if="categories.length > 0"
        :categories="categories"
      />
      
      <!-- Productos destacados -->
      <ProductsSection 
        v-if="productosDestacados.length > 0"
        title="Productos Destacados"
        :products="productosDestacados"
      />
      
      <!-- Loader -->
      <LoadingSpinner v-if="loading" />
    </main>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import BrandsSection from '@/components/home/BrandsSection.vue';
import ProductsSection from '@/components/home/ProductsSection.vue';
import CategoriesSection from '@/components/home/CategoriesSection.vue';
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue';

export default {
  name: 'HomeView',
  components: {
    BrandsSection,
    ProductsSection,
    CategoriesSection,
    LoadingSpinner
  },
  data() {
    return {
      brands: [
        { 
          id: 1, 
          name: 'Nike', 
          image: 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg',
          colorClass: 'nike-color'
        },
        { 
          id: 2, 
          name: 'Samsung', 
          image: 'https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg',
          colorClass: 'samsung-color',
          special: true
        },
        { 
          id: 3, 
          name: 'Coca-Cola', 
          image: 'https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_logo.svg',
          colorClass: 'cocacola-color'
        },
        { 
          id: 4, 
          name: 'Apple', 
          image: 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
          colorClass: 'apple-color'
        },
        { 
          id: 5, 
          name: 'Adidas', 
          image: 'https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg',
          colorClass: 'adidas-color'
        },
        { 
          id: 6, 
          name: 'LG', 
          image: 'https://upload.wikimedia.org/wikipedia/commons/2/20/LG_symbol.svg',
          colorClass: 'lg-color',
          special: true
        }
      ],
      loading: false
    };
  },
  computed: {
    ...mapGetters([
      'todasCategorias',
      'productosDestacados',
      'productosConDescuento'
    ]),
    
    categories() {
      return this.todasCategorias;
    }
  },
  async created() {
    await this.loadData();
  },
  methods: {
    ...mapActions(['cargarCategorias', 'cargarProductos']),
    
    async loadData() {
      this.loading = true;
      try {
        await Promise.all([
          this.cargarCategorias(),
          this.cargarProductos()
        ]);
      } catch (error) {
        console.error('Error cargando datos:', error);
        // Aquí podrías agregar manejo de errores para el usuario
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style lang="scss">
@import '@/assets/styles/variables.scss';
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';

.home-view {
  .main-content {
    padding-top: 2rem;
    padding-bottom: 2rem;
  }
  
  .section-header {
    background-color: white;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    
    .section-title {
      font-size: 1.5rem;
      font-weight: 600;
      color: $text-dark;
      padding-bottom: 0.5rem;
      border-bottom: 3px solid $primary-blue;
      display: inline-block;
      margin-bottom: 0;
    }
  }
}
</style>