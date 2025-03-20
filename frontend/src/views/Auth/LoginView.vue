<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    
    <form @submit.prevent="handleSubmit" class="login-form">
      <div class="input-group">
        <label for="email">Correo electrónico:</label>
        <input
          type="email"
          id="email"
          v-model.trim="email"
          :disabled="isLoading"
          @input="clearError"
          placeholder="ejemplo@correo.com"
        >
      </div>

      <div class="input-group">
        <label for="password">Contraseña:</label>
        <input
          type="password"
          id="password"
          v-model.trim="password"
          :disabled="isLoading"
          minlength="6"
          placeholder="••••••"
          @input="clearError"
        >
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <button 
        type="submit" 
        class="submit-button"
        :class="{ loading: isLoading }"
        :disabled="isLoading"
      >
        <span v-if="!isLoading">Ingresar</span>
        <span v-else>Verificando...</span>
      </button>
    </form>

    <p class="register-link">
      ¿Primera vez aquí? 
      <router-link to="/registro">Crear cuenta</router-link>
    </p>
  </div>
    <p class="password-link">
      ¿Se te ha olvidado la contraseña?
      <router-link to="/Contraseña">Olvidé mi Contraseña</router-link>
    </p>
</template>

<script>
const MOCK_USERS = [
  {
    email: "mauro123@.com",
    password: "123",
    name: "Usuario Demo",
    token: "fake-jwt-token-123"
  }
];

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      isLoading: false,
      errorMessage: ''
    };
  },
  methods: {
    validateForm() {
      if (!this.email || !this.password) {
        this.errorMessage = 'Todos los campos son obligatorios';
        return false;
      }
      
      if (!this.validEmail(this.email)) {
        this.errorMessage = 'Formato de email inválido';
        return false;
      }
      
      return true;
    },
    
    validEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    
    clearError() {
      this.errorMessage = '';
    },
    
    mockAuthService() {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const user = MOCK_USERS.find(u => 
            u.email === this.email.toLowerCase() && 
            u.password === this.password
          );
          
          user ? resolve(user) : reject('Credenciales incorrectas');
        }, 1500);
      });
    },
    
    handleSubmit() {
      if (this.validateForm()) {
        this.isLoading = true;
        
        this.mockAuthService()
          .then(user => {
            console.log('Inicio de sesión exitoso:', user);
            
            // Mostrar notificación con SweetAlert
            this.$swal({
              title: 'Inicio de sesión exitoso',
              text: `Bienvenido, ${user.name}!`,
              icon: 'success',
              confirmButtonColor: '#047ffa',
            }).then(() => {
              // Redirigir al main después de cerrar la alerta
              this.$router.push('/main');
            });
            
            this.errorMessage = '';
          })
          .catch(error => {
            console.error('Error al iniciar sesión:', error);
            this.errorMessage = error;

            // Mostrar error con SweetAlert
            this.$swal({
              title: 'Error al iniciar sesión',
              text: error,
              icon: 'error',
              confirmButtonColor: '#e74c3c',
            });
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  --color-primary: #047ffa;
  --color-error: #e74c3c;
  --color-success: #2ecc71;
  --border-radius: 8px;
  --transition-speed: 0.3s;
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-primary);
  font-weight: 600;
}

input {
  width: 100%;
  padding: 12px;
  border: 2px solid #ecf0f1;
  border-radius: var(--border-radius);
  transition: border-color var(--transition-speed) ease;
}

input:focus {
  border-color: var(--color-primary);
  outline: none;
}

.error-message {
  color: var(--color-error);
  margin: 1rem 0;
  font-size: 0.9rem;
  text-align: center;
}

.success-message {
  color: var(--color-success);
  margin: 1rem 0;
  font-size: 0.9rem;
  text-align: center;
  animation: fadeIn 0.5s ease-in;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: 
    background var(--transition-speed) ease,
    opacity var(--transition-speed) ease;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-link, .password-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
}

.register-link a, .password-link a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
.input-group { 
  margin-bottom: 1.5rem; 
  label { font-weight: bold; color: var(--color-primary); }

}
input { 
  width: 100%; 
  padding: 12px; 
  border-radius: var(--border-radius);
 }
 .submit-button { 
  background-color: var(--color-primary); 
  color: white; 
  padding: 12px; 
  border-radius: var(--border-radius);
 }
 .error-message { 
  color: var(--color-error); 
  text-align: center; 
  margin-top: 1rem; 
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
