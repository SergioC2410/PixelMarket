<template>
  <div class="container mt-5">
    <div class="row">
      <!-- Carrusel de imágenes del producto -->
      <div class="col-md-6">
        <div id="carouselProducto" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner">
            <div 
              v-for="(imagen, index) in producto?.imagenes || []" 
              :key="index" 
              :class="['carousel-item', { active: index === 0 }]"
            >
              <img :src="imagen.url" class="d-block w-100" :alt="producto?.nombre || 'Producto'">
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselProducto" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Anterior</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselProducto" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Siguiente</span>
          </button>
        </div>
      </div>

      <!-- Detalles del producto -->
      <div class="col-md-6">
        <template v-if="producto">
          <h1>{{ producto.nombre }}</h1>
          <p class="text-muted">{{ producto.descripcion }}</p>
          
          <!-- Precio con descuento -->
          <p class="fs-4">
            <strong>Precio:</strong> 
            <span :class="{ 'text-decoration-line-through': producto.descuento }">
              ${{ producto.precio.toFixed(2) }}
            </span>
            <span v-if="producto.descuento" class="text-danger ms-2">
              ${{ precioConDescuento.toFixed(2) }} ({{ producto.descuento }}% OFF)
            </span>
          </p>

          <!-- Clasificación del producto -->
          <p class="text-warning">
            <i class="fas fa-star"></i> {{ producto.clasificacion }} ({{ producto.clasificacion }} estrellas)
          </p>

          <!-- Características -->
          <ul class="list-unstyled">
            <li v-for="(caracteristica, index) in producto.caracteristicas" :key="index">
              <i class="fas fa-check text-success me-2"></i>{{ caracteristica }}
            </li>
          </ul>

          <!-- Botón Agregar al carrito -->
          <button 
            @click="agregarAlCarrito" 
            class="btn btn-primary btn-lg"
            :disabled="agregandoAlCarrito"
          >
            <span v-if="agregandoAlCarrito">
              <i class="fas fa-spinner fa-spin"></i> Agregando...
            </span>
            <span v-else>
              <i class="fas fa-cart-plus"></i> Agregar al carrito
            </span>
          </button>

          <!-- Mensaje de confirmación -->
          <div v-if="mensajeCarrito" class="alert alert-success mt-3">
            {{ mensajeCarrito }}
          </div>
        </template>

        <!-- Mensaje de error si no se cargó el producto -->
        <template v-else>
          <div class="alert alert-danger">
            <strong>Error:</strong> No se pudo cargar la información del producto.
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DetalleProducto',
  data() {
    return {
      producto: null,        // Almacena el producto cargado desde la API
      agregandoAlCarrito: false,
      mensajeCarrito: ''
    };
  },
  computed: {
    // Calcula el precio con descuento si existe
    precioConDescuento() {
      if (!this.producto || !this.producto.descuento) return this.producto?.precio || 0;
      return this.producto.precio * (1 - this.producto.descuento / 100);
    }
  },
  created() {
    this.cargarProducto();
  },
  methods: {
    async cargarProducto() {
      const productoId = this.$route.params.id;
      try {
        // Llamada a la API para obtener el producto
        const respuesta = await axios.get(`https://api.tusitio.com/productos/${productoId}`);
        this.producto = respuesta.data;
      } catch (error) {
        console.error('Error al cargar el producto:', error);
        this.producto = null;
      }
    },
    agregarAlCarrito() {
      this.agregandoAlCarrito = true;
      this.mensajeCarrito = '';

      setTimeout(() => {
        this.mensajeCarrito = '¡Producto agregado al carrito!';
        this.agregandoAlCarrito = false;

        // Limpia el mensaje después de 3 segundos
        setTimeout(() => (this.mensajeCarrito = ''), 3000);
      }, 1000);
    }
  }
};
</script>

<style scoped>
/* Ajusta las imágenes del carrusel */
.carousel-item img {
  max-height: 400px;
  object-fit: contain;
}

/* Estilo del botón deshabilitado */
.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Mensaje de éxito */
.alert-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

/* Precio tachado cuando hay descuento */
.text-decoration-line-through {
  text-decoration: line-through;
}
</style>
