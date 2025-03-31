<template>
  <!-- Fondo interactivo -->
  <div class="interactive-background">
    <!-- Partículas animadas -->
    <div class="particles">
      <div v-for="(particle, index) in particles" :key="index" class="particle" 
           :style="{
             left: particle.x + 'px',
             top: particle.y + 'px',
             width: particle.size + 'px',
             height: particle.size + 'px',
             backgroundColor: particle.color,
             opacity: particle.opacity
           }"></div>
    </div>
    
    <!-- Olas animadas -->
    <div class="waves">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
    </div>
  </div>

  <!-- Contenedor del registro -->
  <div class="register-wrapper">
    <div class="register-container" :class="{ 'shake': hasError }">
      <h2 class="animated-title">Crear nueva cuenta</h2>
      
      <form @submit.prevent="handleRegister" class="register-form animated-form">
        <!-- Campos básicos -->
        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="name">Nombre:</label>
          <input
            type="text"
            id="name"
            v-model.trim="name"
            required
            placeholder="Tu nombre"
            class="animated-input"
          >
          <span class="input-focus-border"></span>
        </div>

        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="lastname">Apellido:</label>
          <input
            type="text"
            id="lastname"
            v-model.trim="lastname"
            required
            placeholder="Tu apellido"
            class="animated-input"
          >
          <span class="input-focus-border"></span>
        </div>

        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="cedula">Cédula:</label>
          <input
            type="text"
            id="cedula"
            v-model.trim="cedula"
            required
            placeholder="Tu número de cédula"
            class="animated-input"
            @input="validateCedula"
          >
          <span class="input-focus-border"></span>
        </div>

        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="email">Correo electrónico:</label>
          <input
            type="email"
            id="email"
            v-model.trim="email"
            required
            placeholder="ejemplo@correo.com"
            class="animated-input"
          >
          <span class="input-focus-border"></span>
        </div>

        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="phone">Teléfono:</label>
          <input
            type="tel"
            id="phone"
            v-model.trim="phone"
            required
            placeholder="+58 123 456 78 90"
            class="animated-input"
            @input="validatePhone"
          >
          <span class="input-focus-border"></span>
        </div>

        <!-- Contraseña -->
        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            v-model.trim="password"
            @input="checkPasswordStrength"
            minlength="8"
            required
            placeholder="••••••••"
            class="animated-input"
          >
          <span class="input-focus-border"></span>
          
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
          
          <transition name="slide-fade">
            <div v-if="showRequirements" class="password-requirements">
              <div 
                v-for="(req, index) in requirements" 
                :key="index"
                :class="['requirement', { 'valid': req.valid }]"
              >
                <svg class="requirement-icon" viewBox="0 0 24 24">
                  <path 
                    fill="currentColor" 
                    :d="req.valid ? 'M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z' 
                    : 'M12,2C6.47,2 2,6.47 2,12C2,17.53 6.47,22 12,22C17.53,22 22,17.53 22,12C22,6.47 17.53,2 12,2Z'" 
                  />
                </svg>
                {{ req.text }}
              </div>
            </div>
          </transition>
        </div>

        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="confirm-password">Confirmar contraseña:</label>
          <input
            type="password"
            id="confirm-password"
            v-model.trim="confirmPassword"
            required
            placeholder="••••••••"
            class="animated-input"
          >
          <span class="input-focus-border"></span>
        </div>

        <!-- Mensaje de error -->
        <transition name="slide-fade">
          <div v-if="errorMessage" class="error-message">
            <svg class="error-icon" viewBox="0 0 24 24">
              <path fill="currentColor" 
              d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
            </svg>
            {{ errorMessage }}
          </div>
        </transition>

        <button 
          type="submit" 
          class="submit-button"
          :disabled="isLoading"
        >
          <span v-if="!isLoading" class="button-content">
            <svg class="button-icon" viewBox="0 0 24 24">
              <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
            </svg>
            <span>Registrarse</span>
          </span>
          <span v-else class="button-content">
            <svg class="spinner" viewBox="0 0 50 50">
              <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
            <span>Registrando...</span>
          </span>
        </button>
      </form>

      <p class="login-link animated-link">
        ¿Ya tienes cuenta? 
        <router-link to="/login">Inicia sesión</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      name: '',
      lastname: '',
      cedula: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      errorMessage: '',
      strengthProgress: 0,
      strengthColor: '#e74c3c',
      strengthText: 'Muy débil',
      hasError: false,
      isLoading: false,
      showRequirements: false,
      particles: Array(30).fill().map(() => ({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 5 + 3,
        color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)`,
        opacity: Math.random() * 0.5 + 0.2,
        speed: Math.random() * 0.5 + 0.2
      }))
    }
  },
  computed: {
    requirements() {
      return [
        { text: 'Mínimo 8 caracteres', valid: this.hasMinLength },
        { text: 'Al menos una mayúscula', valid: this.hasUppercase },
        { text: 'Incluir carácter especial (!@#$%^&*)', valid: this.hasSpecialChar }
      ]
    },
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
    animateParticles() {
      this.particles.forEach(particle => {
        particle.y += particle.speed;
        if (particle.y > window.innerHeight) {
          particle.y = -10;
          particle.x = Math.random() * window.innerWidth;
        }
      });
      
      this.animationFrame = requestAnimationFrame(this.animateParticles);
    },
    resetParticles() {
      this.particles = this.particles.map(particle => ({
        ...particle,
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      }));
    },
    validateCedula() {
      const cedulaRegex = /^[0-9]{6,12}$/
      if (!cedulaRegex.test(this.cedula)) {
        this.errorMessage = 'La cédula debe contener solo números (6-12 dígitos)'
        this.hasError = true
        return false
      }
      return true
    },
    
    validatePhone() {
      const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/
      if (!phoneRegex.test(this.phone)) {
        this.errorMessage = 'Ingresa un número de teléfono válido'
        this.hasError = true
        return false
      }
      return true
    },
    
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
      if (!this.name) {
        this.errorMessage = 'El nombre es obligatorio'
        this.hasError = true
        return false
      }
      
      if (!this.lastname) {
        this.errorMessage = 'El apellido es obligatorio'
        this.hasError = true
        return false
      }
      
      if (!this.validateCedula()) {
        return false
      }
      
      if (!this.validatePhone()) {
        return false
      }
      
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Las contraseñas no coinciden'
        this.hasError = true
        return false
      }
      
      if (!this.hasMinLength) {
        this.errorMessage = 'La contraseña debe tener al menos 8 caracteres'
        this.hasError = true
        return false
      }
      
      if (!this.hasUppercase) {
        this.errorMessage = 'La contraseña debe contener al menos una mayúscula'
        this.hasError = true
        return false
      }
      
      if (!this.hasSpecialChar) {
        this.errorMessage = 'La contraseña debe incluir un carácter especial (!@#$%^&*)'
        this.hasError = true
        return false
      }
      
      this.errorMessage = ''
      this.hasError = false
      return true
    },
    
    handleRegister() {
      if (!this.validateForm()) {
        this.hasError = true;
        setTimeout(() => {
          this.hasError = false;
        }, 1000);
        return;
      }

      this.isLoading = true;
      
      // Simulación de registro
      setTimeout(() => {
        console.log('Datos de registro:', {
          name: this.name,
          lastname: this.lastname,
          cedula: this.cedula,
          email: this.email,
          phone: this.phone,
          password: this.password
        });

        this.$swal({
          title: '¡Registro exitoso!',
          text: 'Ahora puedes iniciar sesión con tus credenciales',
          icon: 'success',
          confirmButtonColor: '#047ffa',
          showClass: {
            popup: 'animate__animated animate__fadeInDown'
          },
          hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
          }
        }).then(() => {
          this.$router.push('/login');
        });
        
        this.isLoading = false;
      }, 1500);
    }
  },
  mounted() {
    this.animateParticles();
    window.addEventListener('resize', this.resetParticles);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resetParticles);
    cancelAnimationFrame(this.animationFrame);
  }
};
</script>

<style scoped>
/* Variables CSS actualizadas */
:root {
  --color-primary: #047ffa;
  --color-primary-light: #4da8ff;
  --color-primary-dark: #0366d6;
  --color-error: #e74c3c;
  --color-error-light: #ff6b6b;
  --color-success: #2ecc71;
  --color-warning: #f1c40f;
  --border-radius: 10px;
  --transition-speed: 0.3s;
  --transition-easing: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Estilos para el fondo interactivo */
.interactive-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  z-index: -1;
  overflow: hidden;
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  border-radius: 50%;
  filter: blur(1px);
  animation: float 15s infinite linear;
}

@keyframes float {
  0% { transform: translateY(0) rotate(0deg); }
  100% { transform: translateY(-100vh) rotate(360deg); }
}

.waves {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  overflow: hidden;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 100%;
  background-repeat: repeat no-repeat;
  background-position: 0 bottom;
  background-size: 50% 100px;
}

.wave-1 {
  animation: wave 15s linear infinite;
  opacity: 0.5;
}

.wave-2 {
  animation: wave 10s linear infinite reverse;
  opacity: 0.3;
}

.wave-3 {
  animation: wave 5s linear infinite;
  opacity: 0.1;
}

@keyframes wave {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* Contenedor del registro */
.register-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 5vh;
  min-height: 100vh;
}

.register-container {
  max-width: 500px;
  width: 90%;
  margin: 0 auto;
  padding: 2.5rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: fadeInUp 0.6s var(--transition-easing);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: fit-content;
  margin-bottom: 2rem;
}

.register-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
}

.register-container.shake {
  animation: shake 0.6s;
}

/* Título animado */
.animated-title {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
  position: relative;
  animation: fadeIn 0.8s ease-out;
}

.animated-title::after {
  content: '';
  display: block;
  width: 50px;
  height: 3px;
  background: var(--color-primary);
  margin: 0.5rem auto 0;
  border-radius: 3px;
}

/* Formulario */
.register-form {
  animation: fadeIn 0.8s ease-out 0.2s both;
}

.input-group {
  margin-bottom: 1.5rem;
  position: relative;
}

label {
  display: block;
  margin-bottom: 0.6rem;
  color: #34495e;
  font-weight: 600;
  font-size: 0.95rem;
}

.animated-input {
  width: 100%;
  padding: 14px 12px;
  border: 2px solid #e0e6ed;
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: all var(--transition-speed) ease;
  background-color: #f8fafc;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.method-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 1em;
}

.animated-input:focus {
  border-color: var(--color-primary);
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(4, 127, 250, 0.2);
  outline: none;
}

.input-focus-border {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-primary);
  transition: width var(--transition-speed) ease;
}

.animated-input:focus ~ .input-focus-border {
  width: 100%;
}

.input-error .animated-input {
  border-color: var(--color-error);
}

.input-error .animated-input:focus {
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.2);
}

.input-error .input-focus-border {
  background-color: var(--color-error);
}

/* Barra de fortaleza de contraseña */
.password-strength {
  margin-top: 8px;
  height: 6px;
  position: relative;
  background-color: #e0e6ed;
  border-radius: 3px;
  overflow: hidden;
}

.strength-bar {
  position: absolute;
  height: 100%;
  border-radius: 3px;
  transition: all var(--transition-speed) ease;
}

.strength-text {
  margin-top: 4px;
  font-size: 0.75rem;
  color: var(--color-text-light);
  text-align: right;
}

/* Requisitos de contraseña */
.password-requirements {
  margin-top: 12px;
  padding: 12px;
  background-color: #f8fafc;
  border-radius: var(--border-radius-sm);
  border-left: 3px solid var(--color-primary-light);
}

.requirement {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  font-size: 0.85rem;
  color: var(--color-text-light);
}

.requirement:last-child {
  margin-bottom: 0;
}

.requirement.valid {
  color: var(--color-success);
}

.requirement-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
}

.requirement.valid .requirement-icon {
  color: var(--color-success);
}

/* Mensaje de error */
.error-message {
  display: flex;
  align-items: center;
  padding: 12px;
  background-color: rgba(231, 76, 60, 0.1);
  color: var(--color-error);
  border-radius: var(--border-radius);
  margin: 1.5rem 0;
  font-size: 0.9rem;
}

.error-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
  flex-shrink: 0;
}

/* Botón de submit */
.submit-button {
  width: 100%;
  padding: 15px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(4, 127, 250, 0.2);
  margin-top: 1rem;
}

.submit-button:hover {
  background: var( 0 6px 8px rgba(7, 51, 95, 0.3));
  box-shadow: 0 6px 8px rgba(4, 127, 250, 0.3);
  transform: translateY(-2px);
}

.submit-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(4, 127, 250, 0.2);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  z-index: 2;
}

.button-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.submit-button:hover .button-icon {
  transform: translateX(3px);
}

.spinner {
  width: 24px;
  height: 24px;
  animation: spin 1.5s linear infinite;
}

.path {
  stroke: white;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

/* Enlaces */
.login-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
  animation: fadeIn 0.8s ease-out;
}

.login-link a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  position: relative;
  transition: color 0.3s ease;
}

.login-link a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width 0.3s ease;
}

.login-link a:hover {
  color: var(--color-primary-dark);
}

.login-link a:hover::after {
  width: 100%;
}

/* Transiciones */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .register-container {
    padding: 2rem;
  }
}

@media (max-width: 480px) {
  .register-container {
    padding: 1.5rem;
    width: 95%;
  }
  
  .animated-input {
    padding: 12px 10px;
  }
  
  .submit-button {
    padding: 14px;
  }
}
</style>