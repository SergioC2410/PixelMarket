<template>
  <div class="container mt-4">
    <!-- Breadcrumbs dinámicos -->
    <b-breadcrumb :items="breadcrumbs" class="mb-4"></b-breadcrumb>

    <!-- Estados de carga -->
    <template v-if="cargando">
      <div class="text-center py-5">
        <b-spinner variant="primary" style="width: 3rem; height: 3rem;"></b-spinner>
        <p class="mt-3">Cargando detalles del producto...</p>
      </div>
    </template>

    <!-- Manejo de errores -->
    <template v-else-if="error">
      <b-alert variant="danger" show class="d-flex align-items-center">
        <div class="flex-grow-1">
          <i class="fas fa-exclamation-circle me-2"></i>
          {{ error }}
        </div>
        <b-button variant="outline-danger" @click="recargarProducto" size="sm">
          <i class="fas fa-sync-alt"></i> Reintentar
        </b-button>
      </b-alert>
    </template>

    <!-- Contenido principal -->
    <template v-else-if="producto">
      <div class="row">
        <!-- Galería de imágenes -->
        <div class="col-lg-6 mb-4 mb-lg-0">
          <div class="sticky-top" style="top: 20px;">
            <b-card no-body class="overflow-hidden shadow-sm">
    <b-carousel 
        id="product-gallery"
        ref="carousel"
        :interval="5000"
        controls
        indicators
        @sliding-start="onSlideChange"
      >
      <!-- Imagen principal -->
      <b-carousel-slide v-if="producto.imagen_url">
        <template #img>
          <img 
            :src="producto.imagen_url" 
            :alt="`${producto.nombre}`"
            class="img-fluid w-100 product-image"
            loading="eager"
            @error="manejarErrorImagen"
          >
        </template>
      </b-carousel-slide>
      
      <b-carousel-slide 
        v-for="(imagen, index) in producto.imagenes_adicionales"
        :key="`product-image-${index}`"
      >
        <template #img>
          <img 
            :src="imagen.url" 
            :alt="`${producto.nombre} - Vista ${index + 2}`"
            class="img-fluid w-100 product-image"
            loading="lazy"
            @error="manejarErrorImagen"
          >
        </template>
      </b-carousel-slide>
      
      <!-- Placeholder solo si no hay imágenes -->
      <b-carousel-slide v-if="!tieneImagenes">
        <template #img>
          <div class="placeholder-image">
            <i class="fas fa-image fa-5x text-muted"></i>
            <p class="mt-2">Imagen no disponible</p>
          </div>
        </template>
      </b-carousel-slide>
    </b-carousel>
            </b-card>
          </div>
        </div>

        <!-- Detalles del producto - Sección derecha -->
        <div class="col-lg-6">
          <b-card no-body class="h-100 border-0">
            <b-card-body>
              <!-- Encabezado con título y SKU -->
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h1 class="h2 mb-0">{{ producto.nombre }}</h1>
                <b-badge variant="light" class="text-dark border">
                  SKU: {{ producto.id }}
                </b-badge>
              </div>

              <!-- Categoría y valoración -->
              <div class="d-flex align-items-center mb-3">
                <b-badge 
                  variant="info" 
                  class="me-2"
                  :to="{ name: 'Productos', query: { categoria: producto.categoria.id } }"
                >
                  {{ producto.categoria.nombre }}
                </b-badge>
                
                <b-form-rating
                  v-model="producto.valoracion_promedio"
                  readonly
                  no-border
                  size="sm"
                  class="p-0 me-2"
                  variant="warning"
                ></b-form-rating>
                
                <small class="text-muted">
                  ({{ producto.cantidad_valoraciones || 0 }} reseñas)
                </small>
              </div>

              <!-- Precio y disponibilidad -->
              <div class="mb-4">
                <div class="d-flex align-items-center">
                  <h4 class="text-primary mb-0">
                    <template v-if="producto.precio_descuento">
                      <span class="text-decoration-line-through text-muted me-2">
                        {{ formatoPrecio(producto.precio) }}
                      </span>
                      <span>{{ formatoPrecio(producto.precio_descuento) }}</span>
                      <b-badge variant="danger" class="ms-2">
                        {{ calcularPorcentajeDescuento(producto) }}% OFF
                      </b-badge>
                    </template>
                    <template v-else>
                      {{ formatoPrecio(producto.precio) }}
                    </template>
                  </h4>
                </div>
                
                <div class="mt-2">
                  <b-badge 
                    :variant="producto.stock > 0 ? 'success' : 'danger'" 
                    pill
                  >
                    <i :class="producto.stock > 0 ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                    {{ producto.stock > 0 ? `Disponible (${producto.stock} unidades)` : 'Agotado' }}
                  </b-badge>
                  
                  <small v-if="producto.stock > 0 && producto.stock <= 10" class="text-warning ms-2">
                    <i class="fas fa-exclamation-triangle"></i> Últimas unidades
                  </small>
                </div>
              </div>

              <!-- Descripción corta -->
              <div class="mb-4">
                <h5 class="mb-2">Descripción</h5>
                <p class="text-muted">{{ producto.descripcion || 'No hay descripción disponible' }}</p>
              </div>

              <!-- Características destacadas -->
              <div class="mb-4" v-if="producto.caracteristicas && producto.caracteristicas.length">
                <h5 class="mb-2">Características principales</h5>
                <ul class="list-unstyled">
                  <li 
                    v-for="(caracteristica, index) in producto.caracteristicas" 
                    :key="`feature-${index}`" 
                    class="mb-2"
                  >
                    <i class="fas fa-check text-success me-2"></i>
                    {{ caracteristica }}
                  </li>
                </ul>
              </div>

              <!-- Selector de cantidad y acciones -->
              <div class="border-top pt-3">
                <div class="d-flex flex-wrap align-items-center gap-3 mb-3">
                  <div class="flex-grow-1" style="max-width: 150px;">
                    <label class="form-label small mb-1" for="cantidad-spinbutton">Cantidad:</label>
                    <b-form-spinbutton 
                      id="cantidad-spinbutton"
                      v-model="cantidad" 
                      min="1" 
                      :max="producto.stock"
                      size="lg"
                      inline
                    ></b-form-spinbutton>
                  </div>
                  
                  <div class="flex-grow-1">
                    <b-button 
                      variant="primary" 
                      size="lg" 
                      @click="agregarAlCarrito"
                      :disabled="producto.stock <= 0 || agregandoAlCarrito"
                      class="w-100"
                    >
                      <template v-if="agregandoAlCarrito">
                        <b-spinner small type="grow" class="me-1"></b-spinner>
                        Agregando...
                      </template>
                      <template v-else>
                        <i class="fas fa-cart-plus me-1"></i>
                        Añadir al carrito
                      </template>
                    </b-button>
                  </div>
                </div>
                
                <b-button 
                  variant="outline-primary" 
                  size="lg" 
                  @click="comprarAhora" 
                  :disabled="producto.stock <= 0"
                  class="w-100 mb-3"
                >
                  <i class="fas fa-bolt me-1"></i>
                  Comprar ahora
                </b-button>
                
                <b-alert
                  v-model="mostrarMensajeCarrito"
                  :variant="mensajeTipo"
                  dismissible
                  fade
                  class="mt-3"
                >
                  {{ mensajeCarrito }}
                </b-alert>
              </div>
            </b-card-body>
          </b-card>
        </div>
      </div>

      <!-- Sección de tabs (descripción, especificaciones, reseñas) -->
      <div class="row mt-4">
        <div class="col-12">
          <b-card no-body class="shadow-sm">
            <b-tabs card lazy>
              <!-- Descripción detallada -->
              <b-tab title="Descripción" active>
                <div class="p-3" v-html="producto.descripcion_larga || 'No hay descripción detallada disponible'"></div>
              </b-tab>
              
              <!-- Especificaciones técnicas -->
              <b-tab title="Especificaciones">
                <div class="p-3">
                  <b-table-simple hover small responsive>
                    <b-tbody>
                      <b-tr v-for="(value, key) in producto.especificaciones" :key="`spec-${key}`">
                        <b-th class="w-25">{{ key }}</b-th>
                        <b-td>{{ value || 'No especificado' }}</b-td>
                      </b-tr>
                    </b-tbody>
                  </b-table-simple>
                </div>
              </b-tab>
              
              <!-- Reseñas -->
              <b-tab title="Reseñas">
                <div class="p-3">
                  <ValoracionesProducto 
                    :producto-id="producto.id" 
                    :valoracion-promedio="producto.valoracion_promedio"
                    :cantidad-valoraciones="producto.cantidad_valoraciones"
                    @valoracion-agregada="actualizarValoraciones"
                  />
                </div>
              </b-tab>
            </b-tabs>
          </b-card>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import ValoracionesProducto from '@/components/ValoracionesProducto.vue';

export default {
  name: 'DetalleProducto',
  components: {
    ValoracionesProducto
  },
  data() {
    return {
      cantidad: 1,
      agregandoAlCarrito: false,
      mensajeCarrito: '',
      mensajeTipo: 'success',
      mostrarMensajeCarrito: false,
      currentSlide: 0
    };
  },
  computed: {
    ...mapGetters(['productoDetalle', 'estaCargando']),
    ...mapState(['error']),
    
    producto() {
      return this.productoDetalle || {};
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
          to: { 
            name: 'Productos', 
            query: { categoria: this.producto.categoria?.id } 
          } 
        },
        { text: this.producto.nombre || 'Detalle', active: true }
      ];
    },
    tieneImagenes() {
      return this.producto.imagen_url || 
            (this.producto.imagenes_adicionales && this.producto.imagenes_adicionales.length > 0);
    }
  },
  methods: {
    ...mapActions(['cargarProductoPorId', 'agregarProductoAlCarrito']),
    
    calcularPorcentajeDescuento(producto) {
      if (!producto.precio_descuento || !producto.precio) return 0;
      return Math.round((1 - producto.precio_descuento / producto.precio) * 100);
    },
    
    formatoPrecio(precio) {
      if (!precio) return '$0.00';
      return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
      }).format(precio);
    },
    
    // Optimización de imágenes
    optimizeImageUrl(url, width = 800) {
      if (!url) return '';
      // Si ya es una URL de Cloudinary o similar con parámetros
      if (url.includes('upload/') && url.includes('image/upload')) {
        return url.replace(/upload\/.*\/(.*)/, `upload/w_${width},q_auto,f_auto/$1`);
      }
      // Para URLs locales
      return url;
    },
    
    generateWebPUrl(url) {
      if (!url) return '';
      return this.optimizeImageUrl(url) + (url.includes('?') ? '&' : '?') + 'format=webp';
    },
    
    async agregarAlCarrito() {
      this.agregandoAlCarrito = true;
      this.mostrarMensajeCarrito = false;
      
      try {
        await this.agregarProductoAlCarrito({
          productoId: this.producto.id,
          cantidad: this.cantidad
        });
        
        this.mensajeTipo = 'success';
        this.mensajeCarrito = `${this.cantidad} ${this.cantidad > 1 ? 'unidades' : 'unidad'} agregadas al carrito`;
        this.mostrarMensajeCarrito = true;
        
        // Evento para analytics
        this.$gtm.trackEvent({
          event: 'add_to_cart',
          ecommerce: {
            items: [{
              item_id: this.producto.id,
              item_name: this.producto.nombre,
              price: this.producto.precio_descuento || this.producto.precio,
              quantity: this.cantidad
            }]
          }
        });
      } catch (error) {
        this.mensajeTipo = 'danger';
        this.mensajeCarrito = error.message || 'Error al agregar al carrito';
        this.mostrarMensajeCarrito = true;
      } finally {
        this.agregandoAlCarrito = false;
      }
    },
    
    comprarAhora() {
      this.agregarAlCarrito().then(() => {
        this.$router.push({ name: 'Carrito' });
      });
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
    
    onSlideChange(slideIndex) {
      this.currentSlide = slideIndex;
    }
  },
  async created() {
    await this.cargarProductoPorId(this.$route.params.id);
  },
  watch: {
    '$route.params.id': {
      handler(newId) {
        if (newId) {
          this.cargarProductoPorId(newId);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      },
      immediate: true
    }
  }
};
</script>

<style scoped>
.sticky-top {
  position: sticky;
  z-index: 1020;
  top: 20px;
}

/* Estilos para el carrusel */
.carousel-img {
  max-height: 500px;
  object-fit: contain;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

/* Miniaturas */
.thumbnail {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  border-radius: 4px;
}

.thumbnail:hover {
  border-color: #007bff;
}

.thumbnail-active {
  border-color: #007bff;
  opacity: 0.8;
}

/* Mejoras de accesibilidad */
[aria-disabled="true"] {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Transiciones suaves */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsividad mejorada */
@media (max-width: 992px) {
  .sticky-top {
    position: static;
  }
  
  .thumbnail {
    width: 50px;
    height: 50px;
  }
}

/* Optimización para móviles */
@media (max-width: 768px) {
  .carousel-img {
    max-height: 300px;
  }
}
</style>