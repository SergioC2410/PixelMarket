<template>
  <div class="card h-100 shadow-sm" @click="verDetalle">
    <img :src="producto.imagen" class="card-img-top" alt="Producto">
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
  methods: {
    verDetalle() {
      this.$router.push({ name: 'DetalleProducto', params: { id: this.producto.id } });
    },
    agregarAlCarrito() {
      // Lógica para agregar al carrito
    }
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
