<template>
  <div>
    <main class="main-content">
      <!-- Sección de marcas -->
      <section class="advertising-section container mb-5 pt-4">
        <h2 class="section-title mb-4">Marcas que trabajan con nosotros</h2>
        <div class="row justify-content-center g-3">
          <div v-for="brand in brands" :key="brand.id" class="col-4 col-sm-3 col-lg-2">
            <div class="brand-card bg-white rounded-3 p-2 shadow-sm">
              <img :src="brand.image" :alt="brand.name" class="brand-logo">
            </div>
          </div>
        </div>
      </section>

      <!-- Sección de descuentos -->
      <section v-if="productosConDescuento.length > 0" class="discounts-section container mb-5">
        <div class="section-header bg-white p-4 rounded-3 shadow-sm">
          <h2 class="section-title mb-0">Descuentos del Día</h2>
        </div>
        <div class="row g-4 mt-2">
          <article v-for="product in productosConDescuento" :key="product.id" class="col-6 col-md-4 col-lg-3">
            <router-link :to="`/productos/${product.id}`" class="text-decoration-none">
              <div class="card h-100 border-0 shadow-hover">
                <img :src="product.imagen_url || 'https://via.placeholder.com/150'" class="card-img-top" :alt="product.nombre">
                <div class="card-body">
                  <h3 class="card-title fs-6">{{ product.nombre }}</h3>
                  <p class="text-danger mb-1 fw-bold">{{ product.descuento_aplicado }}% OFF</p>
                  <p class="text-muted small mb-0"><s>${{ product.precio_original }}</s></p>
                  <p class="text-success fw-bold mb-0">${{ product.precio_con_descuento }}</p>
                </div>
              </div>
            </router-link>
          </article>
        </div>
      </section>

      <!-- Carrusel de categorías -->
      <section v-if="categories.length > 0" class="categories-section container mb-5">
        <div class="section-header bg-white p-4 rounded-3 shadow-sm">
          <h2 class="section-title mb-0">Explorar Categorías</h2>
        </div>
        <div class="position-relative">
          <div id="categoriesCarousel" class="carousel slide mt-2" data-bs-ride="carousel">
            <div class="carousel-inner">
              <div class="carousel-item" v-for="(chunk, index) in chunkedCategories" :key="index" :class="{ active: index === 0 }">
                <div class="row g-3">
                  <article v-for="category in chunk" :key="category.id" class="col-6 col-md-3">
                    <router-link :to="`/productos?categoria=${category.id}`" class="text-decoration-none">
                      <div class="card h-100 border-0 shadow-hover">
                        <img :src="category.imagen || 'https://via.placeholder.com/150'" class="card-img-top" :alt="category.nombre">
                        <div class="card-body text-center">
                          <h3 class="card-title fs-6 mb-0">{{ category.nombre }}</h3>
                        </div>
                      </div>
                    </router-link>
                  </article>
                </div>
              </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#categoriesCarousel" data-bs-slide="prev">
              <span class="carousel-control-prev-icon bg-primary rounded-circle p-3" aria-hidden="true"></span>
              <span class="visually-hidden">Anterior</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#categoriesCarousel" data-bs-slide="next">
              <span class="carousel-control-next-icon bg-primary rounded-circle p-3" aria-hidden="true"></span>
              <span class="visually-hidden">Siguiente</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Productos destacados -->
      <section v-if="productosDestacados.length > 0" class="featured-products-section container mb-5">
        <div class="section-header bg-white p-4 rounded-3 shadow-sm">
          <h2 class="section-title mb-0">Productos Destacados</h2>
        </div>
        <div class="row g-4 mt-2">
          <article v-for="product in productosDestacados" :key="product.id" class="col-6 col-md-4 col-lg-3">
            <router-link :to="`/productos/${product.id}`" class="text-decoration-none">
              <div class="card h-100 border-0 shadow-hover">
                <img :src="product.imagen_url || 'https://via.placeholder.com/150'" class="card-img-top" :alt="product.nombre">
                <div class="card-body">
                  <h3 class="card-title fs-6">{{ product.nombre }}</h3>
                  <p class="text-primary fw-bold mb-0">${{ product.precio }}</p>
                </div>
              </div>
            </router-link>
          </article>
        </div>
      </section>

      <!-- Loader -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'HomeView',
  data() {
    return {
      brands: [
        { id: 1, name: 'Nike', image: 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg' },
        { id: 2, name: 'Samsung', image: 'https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg' },
        { id: 3, name: 'Coca-Cola', image: 'https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_logo.svg' },
        { id: 4, name: 'Apple', image: 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg' },
        { id: 5, name: 'Adidas', image: 'https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg' },
        { id: 6, name: 'LG', image: 'https://upload.wikimedia.org/wikipedia/commons/2/20/LG_symbol.svg' },
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
    },
    
    chunkedCategories() {
      const chunkSize = 4;
      return this.categories.reduce((resultArray, item, index) => {
        const chunkIndex = Math.floor(index / chunkSize);
        if (!resultArray[chunkIndex]) resultArray[chunkIndex] = [];
        resultArray[chunkIndex].push(item);
        return resultArray;
      }, []);
    }
  },
  async created() {
    this.loading = true;
    try {
      await Promise.all([
        this.cargarCategorias(),
        this.cargarProductos()
      ]);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    ...mapActions(['cargarCategorias', 'cargarProductos'])
  }
};
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

:root {
  --primary-blue: #0a80ff;
  --background-blue: #f0f8ff;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--background-blue);
}

/* Navegación */
.navbar-brand { font-size: 1.4rem; }
.nav-link { color: #495057 !important; }
.nav-link:hover { color: var(--primary-blue) !important; }
.nav-link .fa-shopping-cart { font-size: 1.2rem; }
.badge { font-size: 0.6rem; padding: 0.2em 0.4em; }

/* Secciones */
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3436;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--primary-blue);
  display: inline-block;
}

/* Logos de marcas */
.brand-card {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.brand-logo {
  max-width: 80%;
  max-height: 60px;
  object-fit: contain;
  filter: grayscale(100%);
  transition: all 0.3s;
}

.brand-card:hover {
  transform: translateY(-3px);
}

.brand-card:hover .brand-logo {
  filter: grayscale(0%);
}

/* Tarjetas */
.card {
  transition: all 0.3s ease;
  border-radius: 12px !important;
}

.shadow-hover:hover {
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
  transform: translateY(-5px);
}

.card-img-top {
  height: 180px;
  object-fit: contain;
  padding: 1rem;
}

/* Carrusel */
.carousel-control-prev,
.carousel-control-next {
  width: 40px;
  height: 40px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.9;
  z-index: 10;
  margin: auto;
}

.carousel-control-prev { left: -50px; }
.carousel-control-next { right: -50px; }

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-size: 1.2rem;
  background-color: var(--primary-blue);
  border-radius: 50%;
  padding: 1.2rem;
}

@media (max-width: 768px) {
  .carousel-control-prev { left: -15px; }
  .carousel-control-next { right: -15px; }
  .carousel-control-prev-icon,
  .carousel-control-next-icon {
    padding: 0.8rem;
  }
}

/* Loader */
.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>