<template>
    <section class="products-section container mb-5">
      <div class="section-header">
        <h2 class="section-title">{{ title }}</h2>
      </div>
      <div class="row g-4 mt-2">
        <article v-for="product in products" :key="product.id" class="col-6 col-md-4 col-lg-3">
          <router-link :to="`/productos/${product.id}`" class="text-decoration-none">
            <div class="card h-100 border-0 shadow-hover">
              <img 
                :src="product.imagen_url || placeholderImage" 
                class="card-img-top" 
                :alt="product.nombre"
                loading="lazy"
              >
              <div class="card-body">
                <h3 class="card-title fs-6">{{ product.nombre }}</h3>
                <template v-if="showDiscount">
                  <p class="text-danger mb-1 fw-bold">{{ product.descuento_aplicado }}% OFF</p>
                  <p class="text-muted small mb-0"><s>${{ product.precio_original }}</s></p>
                </template>
                <p class="text-success fw-bold mb-0">${{ showDiscount ? product.precio_con_descuento : product.precio }}</p>
              </div>
            </div>
          </router-link>
        </article>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'ProductsSection',
    props: {
      title: {
        type: String,
        required: true
      },
      products: {
        type: Array,
        required: true
      },
      showDiscount: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        placeholderImage: 'https://via.placeholder.com/150'
      };
    }
  };
  </script>
  
  <style lang="scss" scoped>
  @import '@/assets/styles/variables.scss';
  
  .products-section {
    .card {
      transition: all 0.3s ease;
      border-radius: 12px !important;
      
      &:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        transform: translateY(-5px);
      }
    }
    
    .card-img-top {
      height: 180px;
      object-fit: contain;
      padding: 1rem;
    }
  }
  </style>