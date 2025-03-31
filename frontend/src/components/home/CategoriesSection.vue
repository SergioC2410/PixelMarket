<template>
    <section class="categories-section container mb-5">
      <div class="section-header">
        <h2 class="section-title">Explorar Categorías</h2>
      </div>
      <div class="position-relative">
        <div id="categoriesCarousel" class="carousel slide mt-2" data-bs-ride="carousel">
          <div class="carousel-inner">
            <div 
              v-for="(chunk, index) in chunkedCategories" 
              :key="index" 
              class="carousel-item" 
              :class="{ active: index === 0 }"
            >
              <div class="row g-3">
                <article v-for="category in chunk" :key="category.id" class="col-6 col-md-3">
                  <router-link :to="`/productos?categoria=${category.id}`" class="text-decoration-none">
                    <div class="card h-100 border-0 shadow-hover">
                      <img 
                        :src="category.imagen || placeholderImage" 
                        class="card-img-top" 
                        :alt="category.nombre"
                        loading="lazy"
                      >
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
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Anterior</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#categoriesCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Siguiente</span>
          </button>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'CategoriesSection',
    props: {
      categories: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        placeholderImage: 'https://via.placeholder.com/150',
        itemsPerChunk: 4
      };
    },
    computed: {
      chunkedCategories() {
        return this.categories.reduce((resultArray, item, index) => {
          const chunkIndex = Math.floor(index / this.itemsPerChunk);
          if (!resultArray[chunkIndex]) resultArray[chunkIndex] = [];
          resultArray[chunkIndex].push(item);
          return resultArray;
        }, []);
      }
    }
  };
  </script>
  
  <style lang="scss" scoped>
  @import '@/assets/styles/variables.scss';
  
  .categories-section {
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
      background-color: $primary-blue;
      border-radius: 50%;
      padding: 1.2rem;
    }
    
    .card {
      transition: all 0.3s ease;
      
      &:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        transform: translateY(-5px);
      }
    }
    
    .card-img-top {
      height: 150px;
      object-fit: contain;
      padding: 1rem;
    }
    
    @media (max-width: 768px) {
      .carousel-control-prev { left: -15px; }
      .carousel-control-next { right: -15px; }
      
      .carousel-control-prev-icon,
      .carousel-control-next-icon {
        padding: 0.8rem;
      }
    }
  }
  </style>