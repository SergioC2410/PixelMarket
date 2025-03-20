<template>
  <!-- Contenedor principal para el formulario de inicio de sesión -->
  <div class="login-container">
    <!-- Título del formulario -->
    <h2>Iniciar sesión</h2>

    <!-- Formulario de inicio de sesión -->
    <form @submit.prevent="handleSubmit" class="login-form">
      <!-- Grupo de campo para el correo electrónico -->
      <div class="input-group">
        <label for="email">Correo electrónico:</label>
        <input
          type="email"
          id="email"
          v-model.trim="email" 
          :disabled="isLoading" 
          @input="clearError" 
          placeholder="ejemplo@correo.com"
        />
      </div>

      <!-- Grupo de campo para la contraseña -->
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
        />
      </div>

      <!-- Mensaje de error si ocurre un problema durante el inicio de sesión -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Botón para enviar el formulario -->
      <button 
        type="submit" 
        class="submit-button"
        :class="{ loading: isLoading }"
        :disabled="isLoading" 
      >
        <span v-if="!isLoading">Ingresar</span> <!-- Texto del botón cuando no está cargando -->
        <span v-else>Verificando...</span> <!-- Texto del botón cuando está cargando -->
      </button>
    </form>

    <!-- Enlace para registrarse -->
    <p class="register-link">
      ¿Primera vez aquí? 
      <router-link to="/registro">Crear cuenta</router-link>
    </p>

    <!-- Enlace para recuperar la contraseña -->
    <p class="password-link">
      ¿Se te ha olvidado la contraseña?
      <router-link to="/Contraseña">Olvidé mi Contraseña</router-link>
    </p>
  </div>
</template>

<script>
// Simula usuarios registrados para fines de prueba
const MOCK_USERS = [
  {
    email: "mauro123@.com",
    password: "123",
    name: "Usuario Demo",
    token: "fake-jwt-token-123"
  }
];

export default {
  name: 'LoginView', // Nombre del componente

  // Variables reactivas para el estado del formulario
  data() {
    return {
      email: '', // Correo electrónico del usuario
      password: '', // Contraseña del usuario
      isLoading: false, // Estado de carga del formulario
      errorMessage: '' // Mensaje de error
    };
  },

  // Métodos para manejar el formulario
  methods: {
    // Valida que todos los campos estén llenos y que el correo electrónico sea válido
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
    
    // Verifica si un correo electrónico tiene un formato válido
    validEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    
    // Limpia el mensaje de error cuando el usuario interactúa con los campos
    clearError() {
      this.errorMessage = '';
    },
    
    // Simula un servicio de autenticación
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
    
    // Maneja el envío del formulario
    handleSubmit() {
      if (this.validateForm()) {
        this.isLoading = true; // Establece el estado de carga
        
        // Llama al servicio de autenticación simulado
        this.mockAuthService()
          .then(user => {
            console.log('Inicio de sesión exitoso:', user);
            
            // Muestra una notificación de éxito con SweetAlert
            this.$swal({
              title: 'Inicio de sesión exitoso',
              text: `Bienvenido, ${user.name}!`,
              icon: 'success',
              confirmButtonColor: '#047ffa',
            }).then(() => {
              // Redirige al usuario a otra página después de cerrar la alerta
              this.$router.push('/main');
            });
            
            this.errorMessage = ''; // Limpia el mensaje de error
          })
          .catch(error => {
            console.error('Error al iniciar sesión:', error);
            this.errorMessage = error; // Establece el mensaje de error
            
            // Muestra el error con SweetAlert
            this.$swal({
              title: 'Error al iniciar sesión',
              text: error,
              icon: 'error',
              confirmButtonColor: '#e74c3c',
            });
          })
          .finally(() => {
            this.isLoading = false; // Restablece el estado de carga
          });
      }
    }
  }
};
</script>

<style scoped>
/* Variables CSS para colores y estilos */
.login-container {
  --color-primary: #047ffa;
  --color-error: #e74c3c;
  --color-success: #2ecc71;
  --border-radius: 8px;
  --transition-speed: 0.3s;
  max-width: 400px; /* Ancho máximo del contenedor */
  margin: 2rem auto; /* Margen para centrar horizontalmente */
  padding: 2rem; /* Espacio interno */
  background: #fff; /* Fondo blanco */
  border-radius: var(--border-radius); /* Esquinas redondeadas */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra para dar relieve */
}

/* Estilos para los grupos de campos */
.input-group {
  margin-bottom: 1.5rem; /* Espacio entre grupos */
  text-align: left; /* Alineación del texto */
}

/* Estilos para las etiquetas de los campos */
label {
  display: block; /* Etiqueta como bloque */
  margin-bottom: 0.5rem; /* Espacio entre etiqueta y campo */
  color: var(--color-primary); /* Color del texto */
  font-weight: 600; /* Peso de la fuente */
}

/* Estilos para los campos de texto */
input {
  width: 100%; /* Ancho del campo */
  padding: 12px; /* Espacio interno del campo */
  border: 2px solid #ecf0f1; /* Bordes del campo */
  border-radius: var(--border-radius); /* Esquinas redondeadas */
  transition: border-color var(--transition-speed) ease; /* Transición para el color del borde */
}

/* Estilos para el campo cuando tiene foco */
input:focus {
  border-color: var(--color-primary); /* Cambia el color del borde al tener foco */
  outline: none; /* Elimina el contorno */
}

/* Estilos para el mensaje de error */
.error-message {
  color: var(--color-error); /* Color del texto del error */
  margin: 1rem 0; /* Espacio alrededor del mensaje */
  font-size: 0.9rem; /* Tamaño del texto */
  text-align: center; /* Alineación del texto */
}

/* Estilos para el mensaje de éxito */
.success-message {
  color: var(--color-success); /* Color del texto del éxito */
  margin: 1rem 0; /* Espacio alrededor del mensaje */
  font-size: 0.9rem; /* Tamaño del texto */
  text-align: center; /* Alineación del texto */
  animation: fadeIn 0.5s ease-in; /* Animación para aparecer */
}

/* Estilos para el botón de envío */
.submit-button {
  width: 100%; /* Ancho del botón */
  padding: 12px; /* Espacio interno del botón */
  background: var(--color-primary); /* Color de fondo del botón */
  color: white; /* Color del texto del botón */
  border: none; /* Elimina los bordes */
  border-radius: var(--border-radius); /* Esquinas redondeadas */
  cursor: pointer; /* Cursor en forma de mano */
  transition: 
    background var(--transition-speed) ease,
    opacity var(--transition-speed) ease; /* Transición para el color de fondo y opacidad */
}

/* Estilos para el botón cuando está deshabilitado */
.submit-button:disabled {
  opacity: 0.7; /* Opacidad reducida */
  cursor: not-allowed; /* Cursor que indica que no se puede interactuar */
}

/* Estilos para los enlaces de registro y recuperación de contraseña */
.register-link, .password-link {
  margin-top: 1.5rem; /* Espacio superior */
  text-align: center; /* Alineación del texto */
  color: #7f8c8d; /* Color del texto */
}

/* Estilos para los enlaces dentro de los párrafos de registro y recuperación */
.register-link a, .password-link a {
  color: var(--color-primary); /* Color del texto del enlace */
  font-weight: 600; /* Peso de la fuente */
  text-decoration: none; /* Elimina el subrayado */
}

/* Ajustes adicionales para los grupos de campos y campos de texto */
.input-group { 
  margin-bottom: 1.5rem; 
  label { font-weight: bold; 
  color: var(--color-primary); }

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

/* Animación para aparecer */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
