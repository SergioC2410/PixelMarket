<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>

    <form @submit.prevent="handleSubmit" class="login-form">
      <!-- Entrada de correo electrónico -->
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

      <!-- Entrada de contraseña -->
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

      <!-- Mensaje de error -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Botón de envío -->
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

    <p class="password-link">
      ¿Se te ha olvidado la contraseña?
      <router-link to="/Contraseña">Olvidé mi Contraseña</router-link>
    </p>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axiosInstance from "@/util/axios";

export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      isLoading: false,
      errorMessage: "",
    };
  },
  methods: {
    // Validar los campos del formulario
    validateForm() {
      // Verificar que ambos campos están llenos
      if (!this.email || !this.password) {
        this.errorMessage = "Todos los campos son obligatorios";
        return false;
      }

      // Verificar si el formato del correo electrónico es válido
      if (!this.validEmail(this.email)) {
        this.errorMessage = "El correo electrónico no tiene un formato válido";
        return false;
      }

      // Verificar que la contraseña tenga la longitud mínima
      if (this.password.length < 6) {
        this.errorMessage =
          "La contraseña debe tener al menos 6 caracteres";
        return false;
      }

      // Si todo está correcto, no hay errores
      this.errorMessage = "";
      return true;
    },

    // Comprobar el formato del correo electrónico
    validEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Expresión regular para validar correos
      return re.test(email);
    },

    // Limpiar los mensajes de error cuando el usuario escribe
    clearError() {
      this.errorMessage = "";
    },

    // Manejar el envío del formulario
    async handleSubmit() {
      if (this.validateForm()) {
        this.isLoading = true;

        try {
          // Solicitar autenticación al backend
          const response = await axiosInstance.post("/auth/login", {
            email: this.email,
            password: this.password,
          });

          // Extraer token y datos del usuario de la respuesta
          const { token, user } = response.data;

          // Guardar el token en el localStorage
          localStorage.setItem("authToken", token);

          // Mostrar mensaje de éxito con SweetAlert2
          Swal.fire({
            title: "Inicio de sesión exitoso",
            text: `Bienvenido, ${user.username}!`,
            icon: "success",
            confirmButtonColor: "#047ffa",
          }).then(() => {
            // Redirigir al usuario a la página principal
            this.$router.push("/main");
          });

          this.errorMessage = "";
        } catch (error) {
          // Manejo de errores y mostrar el mensaje adecuado
          console.error("Error al iniciar sesión:", error);
          this.errorMessage =
            error.response?.data?.message || "Credenciales incorrectas";

          // Mostrar error con SweetAlert2
          Swal.fire({
            title: "Error al iniciar sesión",
            text: this.errorMessage,
            icon: "error",
            confirmButtonColor: "#e74c3c",
          });
        } finally {
          this.isLoading = false;
        }
      }
    },
  },
};
</script>

<style scoped>
/* Estilos existentes, sin cambios */
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

.submit-button {
  width: 100%;
  padding: 12px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: background var(--transition-speed) ease,
    opacity var(--transition-speed) ease;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-link,
.password-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
}

.register-link a,
.password-link a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
</style>
