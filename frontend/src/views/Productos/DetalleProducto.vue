<template>
  <div class="container mt-5">
    <div class="row">
      <!-- Carrusel de imágenes del producto -->
      <div class="col-md-6">
        <div id="carouselProducto" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner">
            <div 
              v-for="(imagen, index) in producto.imagenes" 
              :key="index" 
              :class="['carousel-item', { active: index === 0 }]"
            >
              <img :src="imagen.url" class="d-block w-100" :alt="producto.nombre || 'Producto'">
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
            <i class="fas fa-star"></i> {{ producto.clasificacion }} estrellas
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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DetalleProducto',
  data() {
    return {
      // Datos ficticios para el producto
      producto: {
        nombre: 'Laptop HP Spectre',
        descripcion: 'Una laptop de alto rendimiento con diseño premium.',
        precio: 1500.00,
        descuento: 20, // Descuento del 20%
        clasificacion: 4.5,
        imagenes: [
          { url: 'https://via.placeholder.com/400x300.png?text=Laptop+Vista+Frontal' },
          { url: 'https://via.placeholder.com/400x300.png?text=Laptop+Vista+Lateral' },
          { url: 'https://via.placeholder.com/400x300.png?text=Laptop+Vista+Posterior' }
        ],
        caracteristicas: [
          'Procesador Intel Core i7 de última generación',
          '16GB RAM',
          'Pantalla táctil 4K UHD',
          '1TB SSD',
          'Batería de larga duración'
        ]
      },
      agregandoAlCarrito: false,
      mensajeCarrito: ''
    };
  },
  computed: {
    // Calcula el precio con descuento si aplica
    precioConDescuento() {
      if (!this.producto || !this.producto.descuento) return this.producto.precio || 0;
      return this.producto.precio * (1 - this.producto.descuento / 100);
    }
  },
  methods: {
    // Simula la acción de agregar el producto al carrito
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
