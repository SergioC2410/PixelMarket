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
                :class="{ 
                  'loading': agregandoAlCarrito,
                  'no-stock': producto.stock <= 0
                }"
                @click="agregarAlCarrito"
                :disabled="producto.stock <= 0 || agregandoAlCarrito"
              >
                <template v-if="!agregandoAlCarrito">
                  <span class="price">{{ formatoPrecio(precioFinal) }}</span>
                  <span class="cart-icon"><i class="fas fa-shopping-cart"></i></span>
                  <span class="buy-text">
                    {{ producto.stock > 0 ? 'Comprar ahora' : 'Agotado' }}
                  </span>
                </template>
                <template v-else>
                  <i class="fas fa-spinner fa-spin loading-spinner"></i>
                  <span class="loading-text">Agregando...</span>
                </template>
              </button>

              <!-- Mensaje flotante -->
              <transition name="message-fade">
                <div v-if="showMessage" class="add-to-cart-message" :class="messageType">
                  <i :class="messageIcon"></i>
                  {{ messageText }}
                </div>
              </transition>
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
import { mapActions, mapGetters, mapState } from 'vuex';
import ValoracionesProducto from '@/components/ValoracionesProducto.vue';

export default {
  name: 'DetalleProducto',
  components: { ValoracionesProducto },
  data() {
    return {
      isHovered: false,
      cantidad: 1,
      agregandoAlCarrito: false,
      placeholderImage: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=',
      showMessage: false,
      messageText: '',
      messageType: 'success',
      messageIcon: 'fas fa-check-circle'
    };
  },
  computed: {
    ...mapGetters(['productoDetalle', 'estaCargando', 'productosConDescuento']),
    ...mapState(['error']),
    
    producto() {
      const productoConDescuento = this.productosConDescuento.find(p => p.id === this.productoDetalle?.id);
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
      return new Intl.NumberFormat('es-VE', {
        style: 'currency',
        currency: 'VES'
      }).format(precio || 0);
    },
    
    async agregarAlCarrito() {
      if (this.producto.stock <= 0) return;
      
      this.agregandoAlCarrito = true;
      
      try {
        await this.agregarProductoAlCarrito({
          productoId: this.producto.id,
          cantidad: this.cantidad,
          precioUnitario: this.precioFinal
        });
        
        this.showFeedback('Producto agregado al carrito', 'success', 'fas fa-check-circle');
        
      } catch (error) {
        const errorMsg = error.response?.data?.message || 
                       error.message || 
                       'Error al agregar al carrito';
        this.showFeedback(errorMsg, 'error', 'fas fa-exclamation-circle');
      } finally {
        this.agregandoAlCarrito = false;
      }
    },
    
    showFeedback(text, type, icon) {
      this.messageText = text;
      this.messageType = type;
      this.messageIcon = icon;
      this.showMessage = true;
      
      setTimeout(() => {
        this.showMessage = false;
      }, 3000);
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
/* ============ ESTILOS GENERALES ============ */
.product-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: white;
  min-height: calc(100vh - 120px);
}

/* ============ ESTILOS DE PRODUCTO ============ */
.product-card {
  width: 100%;
  max-width: 900px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  margin: 1.5rem auto;
  overflow: hidden;
  animation: fadeIn 0.6s ease-out forwards;
}

.product-content {
  display: flex;
  flex-wrap: wrap;
  padding: 2rem;
  gap: 2rem;
}

.product-info {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

/* ============ ESTILOS DE TEXTO ============ */
h1 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  animation: slideIn 0.5s 0.1s ease-out forwards;
}

.description {
  color: #555;
  line-height: 1.6;
  margin: 1.5rem 0;
  animation: fadeIn 0.5s 0.3s ease-out forwards;
}

/* ============ ESTILOS DE DESCUENTO ============ */
.discount-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  animation: fadeIn 0.5s 0.2s ease-out forwards;
}

.discount-percent {
  background-color: #ff4444;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.original-price {
  color: #6c757d;
  text-decoration: line-through;
}

/* ============ ESTILOS DE RATING ============ */
.rating-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  animation: fadeIn 0.5s 0.2s ease-out forwards;
}

.stars {
  color: #FFD700;
  font-size: 1rem;
}

.review-count {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* ============ ESTILOS DE STOCK ============ */
.stock-container {
  margin: 0.5rem 0;
  animation: fadeIn 0.5s 0.4s ease-out forwards;
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

/* ============ ESTILOS DE CANTIDAD ============ */
.quantity-control {
  margin: 1rem 0;
  animation: fadeIn 0.5s 0.5s ease-out forwards;
}

.quantity-control label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #2c3e50;
}

.quantity-selector {
  width: 120px;
}

.quantity-selector .btn {
  padding: 0 0.5rem;
}

/* ============ ESTILOS DEL BOTÓN DE COMPRA ============ */
.buy-button-container {
  margin-top: auto;
  padding: 0 1rem;
  animation: fadeIn 0.5s 0.6s ease-out forwards;
  position: relative;
}

.buy-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #2e28a7 0%, #3a34c9 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0 1.5rem;
  width: 100%;
  height: 50px;
  font-size: 1rem;
  font-weight: 500;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(46, 40, 167, 0.2);
}

.buy-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #3a34c9 0%, #4a44e0 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(46, 40, 167, 0.3);
}

.buy-button:active:not(:disabled) {
  transform: translateY(0);
}

.buy-button.loading {
  background: #6c757d;
  cursor: progress;
}

.buy-button.no-stock {
  background: #6c757d;
  cursor: not-allowed;
}

.buy-button .price {
  font-size: 1.2rem;
  font-weight: bold;
  margin-right: 0.5rem;
}

.buy-button .cart-icon {
  margin-left: 0.5rem;
  font-size: 1.1rem;
}

.buy-button .buy-text {
  flex-grow: 1;
  text-align: center;
}

.loading-spinner {
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

.loading-text {
  flex-grow: 1;
  text-align: center;
}

/* ============ ESTILOS DE IMAGEN ============ */
.product-image-container {
  flex: 1;
  min-width: 300px;
  padding: 1rem;
  animation: fadeIn 0.5s 0.2s ease-out forwards;
}

.image-wrapper {
  position: relative;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-wrapper:hover .product-image {
  transform: scale(1.03);
}

.specs-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(91, 81, 159, 0.9);
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

/* ============ ESTILOS DE MENSAJES ============ */
.add-to-cart-message {
  position: absolute;
  bottom: -40px;
  left: 0;
  right: 0;
  padding: 0.5rem;
  border-radius: 4px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 500;
  z-index: 10;
  opacity: 0.95;
}

.add-to-cart-message.success {
  background-color: #d4edda;
  color: #155724;
}

.add-to-cart-message.error {
  background-color: #f8d7da;
  color: #721c24;
}

.add-to-cart-message i {
  margin-right: 0.5rem;
}

/* ============ ESTILOS DE INFORMACIÓN ADICIONAL ============ */
.additional-info {
  width: 100%;
  max-width: 900px;
  margin-top: 2rem;
}

/* ============ ANIMACIONES ============ */
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.message-fade-enter-active,
.message-fade-leave-active {
  transition: all 0.3s ease;
}

.message-fade-enter-from,
.message-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* ============ MEDIA QUERIES ============ */
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
    height: 300px;
  }
  
  .image-wrapper {
    height: 300px;
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

@media (max-width: 576px) {
  .product-page {
    padding: 1rem;
  }
  
  .product-content {
    padding: 0.5rem;
  }
  
  .product-image-container {
    height: 250px;
  }
  
  .image-wrapper {
    height: 250px;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .description {
    font-size: 0.9rem;
  }
}
</style>