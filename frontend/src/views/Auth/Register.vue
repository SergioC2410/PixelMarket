<template>
    <div class="register-container">
      <h2>Crear nueva cuenta</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="name">Nombre:</label>
          <input
            type="text"
            id="name"
            v-model.trim="name"
            required
            placeholder="Tu nombre completo"
          >
        </div>
  
        <div class="form-group">
          <label for="email">Correo electrónico:</label>
          <input
            type="email"
            id="email"
            v-model.trim="email"
            required
            placeholder="ejemplo@correo.com" 
          >
        </div>
  
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            v-model.trim="password"
            minlength="6"
            required
            placeholder="••••••" 
          >
        </div>
  
        <div class="form-group">
          <label for="confirm-password">Confirmar contraseña:</label>
          <input
            type="password"
            id="confirm-password"
            v-model.trim="confirmPassword"
            required
            placeholder="••••••" 
          >
        </div>
  
        <!-- Mensaje de error -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
  
        <button type="submit" class="submit-button">Registrarse</button>
      </form>
  
      <p class="login-link">
        ¿Ya tienes cuenta? 
        <router-link to="/login">Inicia sesión</router-link>
      </p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RegisterView',
    data() {
      return {
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        errorMessage: ''
      };
    },
    methods: {
      handleRegister() {
        if (!this.validateForm()) return;
  
        // Simulación de registro con datos falsos
        console.log('Datos de registro:', {
          name: this.name,
          email: this.email,
          password: this.password
        });
  
        alert('Registro exitoso. Ahora puedes iniciar sesión.');
        this.$router.push('/login'); // Redirige al login después del registro
      },
      validateForm() {
        if (this.password !== this.confirmPassword) {
          this.errorMessage = 'Las contraseñas no coinciden';
          return false;
        }
        
        if (!this.validEmail(this.email)) {
          this.errorMessage = 'Correo electrónico no válido';
          return false;
        }
  
        this.errorMessage = '';
        return true;
      },
      validEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos similares a los del login */
  .register-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  input {
    width: 100%;
    padding: 12px;
  }
  
  .error-message {
    color: red;
  }
  </style>
  