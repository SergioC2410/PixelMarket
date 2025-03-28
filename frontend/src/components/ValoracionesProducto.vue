<template>
    <div>
      <h5 class="mb-4">Reseñas de clientes</h5>
      
      <div v-if="valoraciones.length === 0" class="alert alert-info">
        Este producto no tiene reseñas aún. ¡Sé el primero en opinar!
      </div>
      
      <div v-else>
        <div v-for="valoracion in valoraciones" :key="valoracion.id" class="mb-4 border-bottom pb-3">
          <div class="d-flex justify-content-between">
            <strong>{{ valoracion.usuario.nombre }}</strong>
            <small class="text-muted">{{ formatFecha(valoracion.fecha) }}</small>
          </div>
          <b-form-rating 
            v-model="valoracion.puntuacion" 
            readonly 
            no-border 
            size="sm"
            class="p-0 my-1"
          ></b-form-rating>
          <p class="mb-1">{{ valoracion.comentario }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      productoId: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        valoraciones: []
      };
    },
    methods: {
      formatFecha(fecha) {
        return new Date(fecha).toLocaleDateString();
      }
    }
  };
  </script>