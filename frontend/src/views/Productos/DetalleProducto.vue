<template>
  <div class="container mt-5">
    <div class="row">
      <!-- Carrusel de imágenes -->
      <div class="col-md-6">
        <div id="carouselProducto" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner">
            <div 
              v-for="(imagen, index) in producto.imagenes" 
              :key="index" 
              :class="['carousel-item', { active: index === 0 }]"
            >
              <img :src="imagen" class="d-block w-100" alt="Imagen del producto">
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
        <h1>{{ producto.nombre }}</h1>
        <p class="text-muted">{{ producto.descripcion }}</p>
        <p class="fs-4">
          <strong>Precio:</strong> ${{ producto.precio }}
          <span v-if="producto.descuento" class="text-danger ms-2">{{ producto.descuento }}% OFF</span>
        </p>
        <p class="text-warning">
          <i class="fas fa-star"></i> {{ producto.clasificacion }} ({{ producto.clasificacion }} estrellas)
        </p>
        <ul class="list-unstyled">
          <li v-for="(caracteristica, index) in producto.caracteristicas" :key="index">
            <i class="fas fa-check text-success me-2"></i>{{ caracteristica }}
          </li>
        </ul>
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
        <div v-if="mensajeCarrito" class="alert alert-success mt-3">
          {{ mensajeCarrito }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DetalleProducto',
  data() {
    return {
      producto: null,
      agregandoAlCarrito: false,
      mensajeCarrito: ''
    };
  },
  created() {
    this.cargarProducto();
  },
  methods: {
    cargarProducto() {
      const productoId = this.$route.params.id;
      // Simulación de carga de producto (reemplazar con Axios)
      this.producto = {
        id: productoId,
        nombre: 'Producto ' + productoId,
        descripcion: 'Descripción del producto ' + productoId,
        precio: 100,
        imagen: 'https://via.placeholder.com/300',
        imagenes: [
          'https://via.placeholder.com/300',
          'https://via.placeholder.com/300',
          'https://via.placeholder.com/300'
        ],
        descuento: 10,
        clasificacion: 4.5,
        caracteristicas: ['Característica 1', 'Característica 2', 'Característica 3']
      };
    },
    agregarAlCarrito() {
      this.agregandoAlCarrito = true; // Mostrar estado de carga
      this.mensajeCarrito = ''; // Reiniciar mensaje

      // Simulación de una llamada asíncrona (reemplazar con Vuex o Axios)
      setTimeout(() => {
        // Lógica para agregar al carrito
        this.mensajeCarrito = '¡Producto agregado al carrito!';
        this.agregandoAlCarrito = false; // Ocultar estado de carga

        // Opcional: Limpiar el mensaje después de unos segundos
        setTimeout(() => {
          this.mensajeCarrito = '';
        }, 3000);
      }, 1000);
    }
  }
};
</script>

<style scoped>
.carousel-item img {
  max-height: 400px;
  object-fit: contain;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.alert-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}
</style>