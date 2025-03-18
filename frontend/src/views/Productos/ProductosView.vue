<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Productos {{ categoriaActual ? `- ${categoriaActual}` : '' }}</h2>
      <button @click="$router.go(-1)" class="btn btn-outline-secondary">
        Volver a categorías
      </button>
    </div>
    
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="producto in productosFiltrados" :key="producto.id">
        <ProductoCard :producto="producto" />
      </div>
    </div>

    <div v-if="productosFiltrados.length === 0" class="alert alert-warning mt-4">
      No hay productos disponibles en esta categoría
    </div>
  </div>
</template>

<script>
import ProductoCard from '@/components/ProductoCard.vue';

export default {
  name: 'ProductosView',
  components: { ProductoCard },
  data() {
    return {
      categoriaActual: this.$route.query.categoria || '',
      productos: [
        // Electrónica
        { 
          id: 1, 
          nombre: 'Smartphone X', 
          precio: 599.99, 
          categoria: 'electrónica',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Teléfono inteligente última generación'
        },
        { 
          id: 2, 
          nombre: 'Laptop Pro', 
          precio: 1299.99, 
          categoria: 'electrónica',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Laptop potente para trabajo y juegos'
        },

        // Hogar
        { 
          id: 3, 
          nombre: 'Sofá Moderno', 
          precio: 899.99, 
          categoria: 'hogar',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Sofá de diseño escandinavo'
        },
        { 
          id: 4, 
          nombre: 'Lámpara de Mesa', 
          precio: 49.99, 
          categoria: 'hogar',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Lámpara moderna para tu sala'
        },

        // Moda
        { 
          id: 5, 
          nombre: 'Zapatos Deportivos', 
          precio: 79.99, 
          categoria: 'moda',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Zapatos cómodos para correr'
        },
        { 
          id: 6, 
          nombre: 'Chaqueta de Cuero', 
          precio: 199.99, 
          categoria: 'moda',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Chaqueta elegante y resistente'
        },

        // Deportes
        { 
          id: 7, 
          nombre: 'Balón de Fútbol', 
          precio: 29.99, 
          categoria: 'deportes',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Balón oficial para partidos'
        },
        { 
          id: 8, 
          nombre: 'Raqueta de Tenis', 
          precio: 89.99, 
          categoria: 'deportes',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Raqueta profesional para tenis'
        },

        // Juguetes
        { 
          id: 9, 
          nombre: 'Lego Classic', 
          precio: 39.99, 
          categoria: 'juguetes',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Set de construcción creativa'
        },
        { 
          id: 10, 
          nombre: 'Muñeca Barbie', 
          precio: 19.99, 
          categoria: 'juguetes',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Muñeca clásica Barbie'
        },

        // Libros
        { 
          id: 11, 
          nombre: 'Cien Años de Soledad', 
          precio: 14.99, 
          categoria: 'libros',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Novela clásica de Gabriel García Márquez'
        },
        { 
          id: 12, 
          nombre: 'El Principito', 
          precio: 9.99, 
          categoria: 'libros',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Libro infantil y filosófico'
        },

        // Belleza
        { 
          id: 13, 
          nombre: 'Kit de Maquillaje', 
          precio: 49.99, 
          categoria: 'belleza',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Kit completo para maquillaje profesional'
        },
        { 
          id: 14, 
          nombre: 'Crema Hidratante', 
          precio: 24.99, 
          categoria: 'belleza',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Crema hidratante para piel seca'
        },

        // Automóviles
        { 
          id: 15, 
          nombre: 'Neumáticos All-Season', 
          precio: 199.99, 
          categoria: 'automóviles',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Neumáticos para todo tipo de clima'
        },
        { 
          id: 16, 
          nombre: 'Aceite de Motor', 
          precio: 29.99, 
          categoria: 'automóviles',
          imagen: 'https://via.placeholder.com/300',
          descripcion: 'Aceite sintético para motor'
        }
      ]
    };
  },
  computed: {
    productosFiltrados() {
      if (!this.categoriaActual) return this.productos;
      return this.productos.filter(p => 
        p.categoria.toLowerCase() === this.categoriaActual.toLowerCase()
      );
    }
  }
};
</script>

<style scoped>
/* Estilos específicos para la página de productos */
</style>