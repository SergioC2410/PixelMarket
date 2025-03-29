<template>
  <div class="search-results-container">
    <div class="search-header">
      <h2 class="search-title">Resultados para: <span class="search-query">"{{ query }}"</span></h2>
      <p class="results-count">{{ results.length }} resultados encontrados</p>
    </div>

    <div class="results-grid">
      <div 
        v-for="result in results" 
        :key="result.id" 
        class="result-card"
        @click="viewProduct(result)"
      >
        <div class="product-image">
          <img :src="result.image || placeholderImage" :alt="result.name" />
        </div>
        <div class="product-info">
          <h3 class="product-name">{{ result.name }}</h3>
          <p class="product-description">{{ result.description || 'Descripción no disponible' }}</p>
          <div class="product-footer">
            <span class="product-price">${{ result.price?.toFixed(2) || '0.00' }}</span>
            <button class="add-to-cart-btn" @click.stop="addToCart(result)">
              <i class="fas fa-cart-plus"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="results.length === 0" class="no-results">
      <i class="fas fa-search fa-3x"></i>
      <h3>No encontramos resultados para "{{ query }}"</h3>
      <p>Intenta con términos diferentes o revisa la ortografía</p>
      <button class="back-btn" @click="$router.go(-1)">Volver atrás</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchResults',
  props: {
    query: String
  },
  data() {
    return {
      results: [],
      placeholderImage: 'https://via.placeholder.com/300x200?text=Producto'
    };
  },
  mounted() {
    // Simulación de búsqueda con datos más completos
    this.results = [
      {
        id: 1,
        name: 'Teclado Mecánico RGB',
        description: 'Teclado gaming con switches azules y retroiluminación RGB',
        price: 89.99,
        image: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3'
      },
      {
        id: 2,
        name: 'Mouse Inalámbrico',
        description: 'Mouse ergonómico con sensor de alta precisión 16000 DPI',
        price: 45.50,
        image: 'https://images.unsplash.com/photo-1527814050087-3793815479db',
      },
      {
        id: 3,
        name: 'Monitor 24" Full HD',
        description: 'Monitor IPS con 144Hz de refresco y tiempo de respuesta 1ms',
        price: 199.99,
        image: 'https://nuweapp.com/media/catalog/product/3/4/34.png?auto=webp&format=png&width=640&height=800&fit=cover'
      },
      {
        id: 4,
        name: 'Auriculares Gaming',
        description: 'Sonido surround 7.1 con micrófono retráctil',
        price: 75.00,
        image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e'
      }
    ];
  },
  methods: {
    viewProduct(product) {
      console.log('Ver producto:', product);
      // this.$router.push({ name: 'product', params: { id: product.id } });
    },
    addToCart(product) {
      console.log('Añadir al carrito:', product);
      // Lógica para añadir al carrito
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

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.result-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.product-image {
  height: 200px;
  overflow: hidden;
  background: #f5f5f5;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.result-card:hover .product-image img {
  transform: scale(1.05);
}

.product-info {
  padding: 1.2rem;
}

.product-name {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.product-description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.product-price {
  color: var(--color-primary);
  font-weight: 700;
  font-size: 1.1rem;
}

.add-to-cart-btn {
  background: var(--color-primary);
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-to-cart-btn:hover {
  background: var(--color-primary-light);
  transform: scale(1.1);
}

.no-results {
  text-align: center;
  padding: 3rem 0;
  color: #666;
}

.no-results i {
  color: #ddd;
  margin-bottom: 1rem;
}

.no-results h3 {
  color: #444;
  margin-bottom: 0.5rem;
}

.back-btn {
  background: var(--color-primary);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 30px;
  margin-top: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.back-btn:hover {
  background: var(--color-primary-light);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(4, 127, 250, 0.3);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .search-title {
    font-size: 1.5rem;
  }
  
  .results-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }
}
</style>