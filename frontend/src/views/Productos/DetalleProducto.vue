<template>
  <div class="product-page">
    <!-- Breadcrumbs dinámicos -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4"></b-breadcrumb>

    <!-- Estados de carga -->
    <template v-if="cargando">
      <div class="text-center py-5">
        <b-spinner variant="primary"></b-spinner>
        <p class="mt-3">Cargando detalles...</p>
      </div>
    </template>

    <!-- Manejo de errores -->
    <b-alert v-else-if="error" variant="danger" show class="d-flex align-items-center">
      <div class="flex-grow-1">
        <i class="fas fa-exclamation-circle me-2"></i>
        {{ error }}
      </div>
      <b-button variant="outline-danger" @click="recargarProducto" size="sm">
        <i class="fas fa-sync-alt"></i> Reintentar
      </b-button>
    </b-alert>

    <!-- Contenido principal -->
    <template v-else-if="producto">
      <div class="product-card">
        <div class="product-content">
          <!-- Detalles del producto -->
          <div class="product-info">
            <h1>{{ producto.nombre }}</h1>
            
            <!-- Mostrar descuento si existe -->
            <div v-if="tieneDescuento" class="discount-badge">
              <span class="discount-percent">{{ producto.descuento_aplicado }}% OFF</span>
              <span class="original-price">
                <s>{{ formatoPrecio(producto.precio_original) }}</s>
              </span>
            </div>
            
            <div class="rating-container">
              <span class="stars">
                <i v-for="star in 5" :key="star" 
                  :class="getStarClass(star, producto.valoracion_promedio)" 
                  aria-hidden="true"></i>
              </span>
              <span class="review-count">({{ producto.cantidad_valoraciones }} reseñas)</span>
            </div>

            <p class="description">{{ producto.descripcion || 'Descripción no disponible' }}</p>

            <div class="stock-container">
              <span :class="['stock-badge', producto.stock > 0 ? 'in-stock' : 'out-of-stock']">
                {{ producto.stock > 0 ? `Disponible (${producto.stock})` : 'Agotado' }}
              </span>
            </div>

            <div class="quantity-control">
              <label for="cantidad-selector">Cantidad</label>
              <b-form-spinbutton 
                id="cantidad-selector"
                v-model="cantidad" 
                min="1" 
                :max="producto.stock"
                class="quantity-selector"
              ></b-form-spinbutton>
            </div>

            <div class="buy-button-container">
              <button 
                class="buy-button"
                @mouseenter="isHovered = true"
                @mouseleave="isHovered = false"
                @click="agregarAlCarrito"
                :disabled="producto.stock <= 0 || agregandoAlCarrito"
              >
                <span class="price">
                  {{ formatoPrecio(precioFinal) }}
                </span>
                <span class="cart-icon">
                  <i class="fas fa-shopping-cart"></i>
                </span>
                <span class="buy-text">
                  {{ agregandoAlCarrito ? 'Agregando...' : 'Comprar ahora' }}
                </span>
              </button>
            </div>
          </div>

          <!-- Imagen del producto -->
          <div class="product-image-container">
            <div class="image-wrapper">
              <img 
                :src="producto.imagen_url || placeholderImage" 
                :alt="producto.nombre"
                @error="manejarErrorImagen"
                class="product-image"
              >
              
              <div class="specs-overlay">
                <h3>Especificaciones</h3>
                <ul>
                  <li v-for="(value, key) in producto.especificaciones" :key="key">
                    <strong>{{ key }}:</strong> {{ value || 'N/A' }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección de tabs -->
      <div class="additional-info">
        <b-card>
          <b-tabs>
            <b-tab title="Reseñas">
              <ValoracionesProducto 
                :producto-id="producto.id"
                @valoracion-agregada="actualizarValoraciones"
              />
            </b-tab>
          </b-tabs>
        </b-card>
      </div>
    </template>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import ValoracionesProducto from '@/components/ValoracionesProducto.vue'

export default {
  name: 'DetalleProducto',
  components: { ValoracionesProducto },
  data() {
    return {
      isHovered: false,
      cantidad: 1,
      agregandoAlCarrito: false,
      placeholderImage: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
    }
  },
  computed: {
    ...mapGetters(['productoDetalle', 'estaCargando', 'productosConDescuento']),
    ...mapState(['error']),
    
    producto() {
      // Buscar si el producto tiene descuento en el store
      const productoConDescuento = this.productosConDescuento.find(p => p.id === this.productoDetalle?.id);
      
      // Si tiene descuento, mezclar los datos
      return productoConDescuento || this.productoDetalle || {};
    },
    
    tieneDescuento() {
      return !!this.producto.descuento_aplicado;
    },
    
    precioFinal() {
      return this.tieneDescuento 
        ? this.producto.precio_con_descuento 
        : this.producto.precio;
    },
    
    cargando() {
      return this.estaCargando;
    },
    
    breadcrumbs() {
      return [
        { text: 'Inicio', to: '/' },
        { text: 'Productos', to: { name: 'Productos' } },
        { 
          text: this.producto.categoria?.nombre || 'Categoría', 
          to: { name: 'Productos', query: { categoria: this.producto.categoria?.id } }
        },
        { text: this.producto.nombre || 'Detalle', active: true }
      ];
    }
  },
  methods: {
    ...mapActions(['cargarProductoPorId', 'agregarProductoAlCarrito']),
    
    formatoPrecio(precio) {
      return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
      }).format(precio || 0);
    },
    
    async agregarAlCarrito() {
      this.agregandoAlCarrito = true;
      try {
        await this.agregarProductoAlCarrito({
          productoId: this.producto.id,
          cantidad: this.cantidad,
          precioUnitario: this.precioFinal // Enviamos el precio con descuento si aplica
        });
        this.$bvToast.toast('Producto agregado al carrito', {
          variant: 'success',
          autoHideDelay: 3000
        });
      } catch (error) {
        this.$bvToast.toast(error.message, {
          variant: 'danger',
          autoHideDelay: 3000
        });
      } finally {
        this.agregandoAlCarrito = false;
      }
    },
    
    recargarProducto() {
      this.cargarProductoPorId(this.$route.params.id);
    },
    
    actualizarValoraciones({ promedio, cantidad }) {
      this.$store.commit('ACTUALIZAR_PRODUCTO', {
        ...this.producto,
        valoracion_promedio: promedio,
        cantidad_valoraciones: cantidad
      });
    },
    
    manejarErrorImagen(event) {
      event.target.src = this.placeholderImage;
    },
    
    getStarClass(starIndex, rating) {
      const ratingValue = rating || 0;
      if (starIndex <= ratingValue) {
        return 'fas fa-star';
      }
      if (starIndex - 0.5 <= ratingValue) {
        return 'fas fa-star-half-alt';
      }
      return 'far fa-star';
    }
  },
  async created() {
    await this.cargarProductoPorId(this.$route.params.id);
  },
  watch: {
    '$route.params.id': {
      handler(newId) {
        if (newId) this.cargarProductoPorId(newId);
      },
      immediate: true
    }
  }
};
</script>


<style scoped>
/* Base styles */
.product-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: white;
}

/* Container */
.product-card {
  width: 750px;
  height: 450px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  margin: 1.5rem auto;
  overflow: hidden;
  opacity: 0;
  animation: fadeIn 0.6s ease-out forwards;
}

/* Content grid */
.product-content {
  display: flex;
  height: 100%;
  padding: 1.5rem;
  gap: 2rem;
}

/* Left column (info) */
.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

/* Text styles */
h1 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  animation: slideIn 0.5s 0.1s ease-out forwards;
  opacity: 0;
}

.description {
  color: #555;
  line-height: 1.6;
  text-align: center;
  margin: 1.5rem 0;
  padding: 0 1rem;
  animation: fadeIn 0.5s 0.3s ease-out forwards;
  opacity: 0;
}

/* Rating */
.rating-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  animation: fadeIn 0.5s 0.2s ease-out forwards;
  opacity: 0;
}

.stars {
  color: #FFD700;
  font-size: 1rem;
}

.review-count {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* Descuento */
.discount-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  animation: fadeIn 0.5s 0.2s ease-out forwards;
  opacity: 0;
}

.discount-percent {
  background-color: #ff4444;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.9rem;
}

.original-price {
  color: #6c757d;
  font-size: 0.9rem;
}

/* Stock */
.stock-container {
  margin: 0.5rem 0;
  animation: fadeIn 0.5s 0.4s ease-out forwards;
  opacity: 0;
  text-align: center;
}

.stock-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
  color: white;
}

.stock-badge.in-stock {
  background: #151bc5c5;
}

.stock-badge.out-of-stock {
  background: #dc3545;
}

/* Quantity */
.quantity-control {
  display: none;
  margin: 1rem 0;
  animation: fadeIn 0.5s 0.5s ease-out forwards;
  opacity: 0;
}

.quantity-control label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #2c3e50;
}

/* Button */
.buy-button-container {
  margin-top: auto;
  padding: 0 1rem;
  animation: fadeIn 0.5s 0.6s ease-out forwards;
  opacity: 0;
}

.buy-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #2e28a7;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0;
  width: 100%;
  height: 50px;
  font-size: 1rem;
  font-weight: 500;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.buy-button:hover {
  background: #218838;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(40, 167, 69, 0.25);
}

.buy-button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.buy-button .price {
  padding: 0 1.5rem;
  height: 100%;
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  font-size: 1.4rem;
  font-weight: bold;
  color: white;
}

.buy-button .cart-icon {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translateX(-100%);
  opacity: 0;
  transition: all 0.3s ease;
  font-size: 1.2rem;
}

.buy-button .buy-text {
  flex: 1;
  text-align: center;
}

.buy-button:hover .price {
  transform: translateX(-100%);
  opacity: 0;
}

.buy-button:hover .cart-icon {
  transform: translateX(0);
  opacity: 1;
}

/* Right column (image) */
.product-image-container {
  flex: 1;
  padding: 1rem;
  animation: fadeIn 0.5s 0.2s ease-out forwards;
  opacity: 0;
}

.image-wrapper {
  position: relative;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 110%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-wrapper:hover .product-image {
  transform: scale(1.03);
}

/* Specs overlay */
.specs-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(91, 81, 159, 0.378);
  color: white;
  padding: 1.5rem;
  transform: translateY(100%) rotateX(15deg);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow-y: auto;
}

.specs-overlay h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  text-align: center;
}

.specs-overlay ul {
  list-style: none;
  padding: 0;
}

.specs-overlay li {
  margin: 0.8rem 0;
  padding: 0.6rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
}

.image-wrapper:hover .specs-overlay {
  transform: translateY(0) rotateX(0);
  opacity: 1;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive */
@media (max-width: 800px) {
  .product-card {
    width: 100%;
    height: auto;
  }
  
  .product-content {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  
  .product-image-container {
    padding: 0;
    height: 250px;
  }
  
  .description {
    padding: 0;
  }

  .discount-badge {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .buy-button {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
}
</style>