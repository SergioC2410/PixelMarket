<template>
  <div class="card h-100 shadow-sm" @click="verDetalle">
    <!-- Cambio clave: usar producto.imagen_url y agregar manejo de errores -->
    <img 
      :src="producto.imagen_url || placeholderImage" 
      class="card-img-top product-image"
      :alt="producto.nombre"
      @error="manejarErrorImagen"
    >
    <div class="card-body">
      <h5 class="card-title">{{ producto.nombre }}</h5>
      <p class="card-text text-muted">{{ producto.descripcion }}</p>
      <div class="d-flex justify-content-between align-items-center">
        <span class="h5 text-primary">${{ producto.precio }}</span>
        <button @click.stop="agregarAlCarrito" class="btn btn-primary">
          <i class="fas fa-cart-plus"></i>
        </button>
      </div>
      <button @click.stop="verDetalle" class="btn btn-link mt-2">
        Ver detalles
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductoCard',
  props: {
    producto: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      placeholderImage: require('@/assets/placeholder-producto.png') // Agregar imagen de respaldo
    }
  },
  methods: {
    verDetalle() {
      this.$router.push({ name: 'DetalleProducto', params: { id: this.producto.id } });
    },
    agregarAlCarrito() {
      // Lógica para agregar al carrito
    },
    // Nuevo método para manejar errores de imagen
    manejarErrorImagen(event) {
      console.error('Error cargando imagen:', event.target.src);
      event.target.src = this.placeholderImage;
      event.target.classList.add('error-imagen');
    }
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  overflow: hidden; /* Para contener la imagen */
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-image {
  height: 250px;
  object-fit: cover; /* Mantener relación de aspecto */
  transition: transform 0.3s ease;
}

.product-image:hover {
  transform: scale(1.05);
}

.error-imagen {
  background-color: #f8f9fa;
  padding: 1rem;
}

.btn-link {
  text-decoration: none;
}
</style>