<template>
    <section class="brands-section container mb-5 pt-4">
      <h2 class="section-title mb-4">Marcas que trabajan con nosotros</h2>
      <div class="row justify-content-center g-3">
        <div v-for="brand in brands" :key="brand.id" class="col-4 col-sm-3 col-lg-2">
          <div class="brand-card" :class="brand.colorClass">
            <img 
              :src="brand.image" 
              :alt="brand.name" 
              class="brand-logo"
              :class="{ 'special-logo': brand.special }"
            >
          </div>
        </div>
      </div>  
    </section>
  </template>
  
  <script>
  export default {
    name: 'BrandsSection',
    props: {
      brands: {
        type: Array,
        required: true
      }
    }
  };
  </script>
  
  <style lang="scss" scoped>
  @import '@/assets/styles/variables.scss';
  
  .brands-section {
    .brand-card {
      height: 100px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
      background-color: white;
      border-radius: 8px;
      padding: 15px;
      position: relative;
      overflow: hidden;
      
      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1;
      }
      
      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        
        .brand-logo {
          filter: brightness(0) invert(1);
        }
        
        &::before {
          opacity: 1;
        }
      }
    }
    
    .brand-logo {
      max-width: 80%;
      max-height: 60px;
      object-fit: contain;
      transition: all 0.3s ease;
      filter: grayscale(100%) brightness(0.5);
      position: relative;
      z-index: 2;
    }
    
    // Colores específicos para cada marca
    .nike-color::before {
      background-color: #111111;
    }
    
    .samsung-color::before {
      background-color: #1428A0;
    }
    
    .cocacola-color::before {
      background-color: #F40009;
    }
    
    .apple-color::before {
      background-color: #A2AAAD;
    }
    
    .adidas-color::before {
      background-color: #006F42;
    }
    
    .lg-color::before {
      background-color: #A50034;
    }
    
    // Estilos para logos especiales
    .special-logo {
      filter: grayscale(100%) brightness(0.5) !important;
    }
    
    .samsung-color:hover .special-logo {
      filter: none !important;
      background-color: #1428A0;
      padding: 10px;
      border-radius: 4px;
    }
    
    .lg-color:hover .special-logo {
      filter: none !important;
      background-color: #A50034;
      padding: 5px;
      border-radius: 50%;
    }
  }
  </style>