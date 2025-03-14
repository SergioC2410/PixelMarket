<template>
    <div class="container mt-5">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="login">
        <!-- Campo de correo electrónico -->
        <div class="mb-3">
          <label for="email" class="form-label">Correo electrónico</label>
          <input 
            type="email" 
            class="form-control" 
            id="email" 
            v-model="email" 
            required
          >
        </div>
  
        <!-- Campo de contraseña -->
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input 
            type="password" 
            class="form-control" 
            id="password" 
            v-model="password" 
            required
          >
        </div>
  
        <!-- Botón de envío -->
        <button type="submit" class="btn btn-primary">Ingresar</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginView',
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      login() {
        // Lógica para iniciar sesión (usar Axios)
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos específicos para la página de login */
  </style>