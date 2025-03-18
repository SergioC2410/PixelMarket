<!-- eslint-disable vue/multi-word-component-names -->
<template>
   <div class="register-container">
    <h2>Crear nueva cuenta</h2>
    <form @submit.prevent="handleRegister">
      <div class="input-group">
        <label for="name">Nombre:</label>
        <input
          type="text"
          id="name"
          v-model.trim="name"
          required
          placeholder="Tu nombre completo"
        >
      </div>

      <div class="input-group">
        <label for="email">Correo electrónico:</label>
        <input
          type="email"
          id="email"
          v-model.trim="email"
          required
          placeholder="ejemplo@correo.com" 
        >
      </div>

      <div class="input-group">
        <label for="password">Contraseña:</label>
        <input
          type="password"
          id="password"
          v-model.trim="password"
          @input="checkPasswordStrength"
          minlength="8"
          required
          placeholder="••••••••"
        >
        
        <!-- Barra de seguridad -->
        <div class="password-strength">
          <div 
            class="strength-bar"
            :style="{
              width: strengthProgress + '%',
              backgroundColor: strengthColor
            }"
          ></div>
          <div class="strength-text">{{ strengthText }}</div>
        </div>
        
        <!-- Requisitos de contraseña -->
        <div class="password-requirements">
          <div :class="['requirement', { 'valid': hasMinLength }]">
            {{ hasMinLength ? '✓' : '•' }} Mínimo 8 caracteres
          </div>
          <div :class="['requirement', { 'valid': hasUppercase }]">
            {{ hasUppercase ? '✓' : '•' }} Al menos una mayúscula
          </div>
          <div :class="['requirement', { 'valid': hasSpecialChar }]">
            {{ hasSpecialChar ? '✓' : '•' }} Incluir carácter especial (!@#$%^&*)
          </div>
        </div>
      </div>

      <div class="input-group">
        <label for="confirm-password">Confirmar contraseña:</label>
        <input
          type="password"
          id="confirm-password"
          v-model.trim="confirmPassword"
          required
          placeholder="••••••••" 
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
      errorMessage: '',
      strengthProgress: 0,
      strengthColor: '#e74c3c',
      strengthText: 'Muy débil'
    }
  },
  computed: {
    hasMinLength() {
      return this.password.length >= 8
    },
    hasUppercase() {
      return /[A-Z]/.test(this.password)
    },
    hasSpecialChar() {
      return /[!@#$%^&*]/.test(this.password)
    }
  },
  methods: {
    checkPasswordStrength() {
      const requirementsMet = [
        this.hasMinLength,
        this.hasUppercase,
        this.hasSpecialChar,
        this.password.length >= 12
      ].filter(Boolean).length

      this.strengthProgress = (requirementsMet / 4) * 100
      
      if (requirementsMet === 4) {
        this.strengthColor = '#2ecc71'
        this.strengthText = 'Muy segura'
      } else if (requirementsMet >= 2) {
        this.strengthColor = '#f1c40f'
        this.strengthText = 'Moderada'
      } else {
        this.strengthColor = '#e74c3c'
        this.strengthText = 'Débil'
      }
    },
    
    validateForm() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Las contraseñas no coinciden'
        return false
      }
      
      if (!this.hasMinLength) {
        this.errorMessage = 'La contraseña debe tener al menos 8 caracteres'
        return false
      }
      
      if (!this.hasUppercase) {
        this.errorMessage = 'La contraseña debe contener al menos una mayúscula'
        return false
      }
      
      if (!this.hasSpecialChar) {
        this.errorMessage = 'La contraseña debe incluir un carácter especial (!@#$%^&*)'
        return false
      }
      
      this.errorMessage = ''
      return true
    },
    
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
    }
  }
};
</script>
  
  <style scoped>
  .register-container {
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

.password-strength {
  margin-top: 0.5rem;
  height: 5px;
  background: #ecf0f1;
  border-radius: var(--border-radius);
  overflow: hidden;
}

.strength-bar {
  height: 100%;
  transition: 
    width var(--transition-speed) ease,
    background-color var(--transition-speed) ease;
}

.strength-text {
  font-size: 0.8rem;
  color: #7f8c8d;
  margin-top: 0.5rem;
  text-align: right;
}

.password-requirements {
  margin-top: 1rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: var(--border-radius);
}

.requirement {
  color: #e74c3c;
  font-size: 0.85rem;
  margin: 0.3rem 0;
  transition: color var(--transition-speed) ease;
}

.requirement.valid {
  color: #2ecc71;
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

.login-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
}

.login-link a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
</style>
  