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

  <!-- Contenedor del login centrado arriba -->
  <div class="login-wrapper">
    <div class="login-container" :class="{ 'shake': hasError }">
      <!-- Logo de la empresa -->
      <div class="logo-container">
         <img src="@/assets/Logo/logo.png" alt="PixelMarket Logo" class="logo">
          <path fill="var(--color-primary)" d="M12,3L2,12H5V20H19V12H22L12,3M12,7.7C14.1,7.7 15.8,9.4 15.8,11.5C15.8,13.6 14.1,15.3 12,15.3C9.9,15.3 8.2,13.6 8.2,11.5C8.2,9.4 9.9,7.7 12,7.7M7,18V10H17V18H7Z" />

      </div>

      <h2 class="animated-title">Iniciar sesión</h2>

      <form @submit.prevent="handleSubmit" class="login-form animated-form">
        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="email">Correo electrónico:</label>
          <input
            type="email"
            id="email"
            v-model.trim="email" 
            :disabled="isLoading" 
            @input="clearError" 
            placeholder="ejemplo@correo.com"
            class="animated-input"
          />
          <span class="input-focus-border"></span>
        </div>

        <div class="input-group" :class="{ 'input-error': hasError }">
          <label for="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            v-model.trim="password" 
            :disabled="isLoading" 
            minlength="6" 
            placeholder="••••••"
            @input="clearError" 
            class="animated-input"
          />
          <span class="input-focus-border"></span>
        </div>

        <transition name="slide-fade">
          <div v-if="errorMessage" class="error-message">
            <svg class="error-icon" viewBox="0 0 24 24">
              <path fill="currentColor" d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
            </svg>
            {{ errorMessage }}
          </div>
        </transition>

        <button 
          type="submit" 
          class="submit-button"
          :class="{ loading: isLoading }"
          :disabled="isLoading" 
        >
          <span v-if="!isLoading" class="button-content">
            <svg class="button-icon" viewBox="0 0 24 24">
              <path fill="currentColor" d="M10,17V14H3V10H10V7L15,12L10,17M10,2H19A2,2 0 0,1 21,4V20A2,2 0 0,1 19,22H10A2,2 0 0,1 8,20V18H10V20H19V4H10V6H8V4A2,2 0 0,1 10,2Z" />
            </svg>
            <span>Ingresar</span>
          </span>
          <span v-else class="button-content">
            <svg class="spinner" viewBox="0 0 50 50">
              <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
            <span>Verificando...</span>
          </span>
        </button>
      </form>

      <p class="register-link animated-link">
        ¿Primera vez aquí? 
        <router-link to="/registro">Crear cuenta</router-link>
      </p>

      <p class="password-link animated-link">
        ¿Se te ha olvidado la contraseña?
        <router-link to="/contraseña">Olvidé mi Contraseña</router-link>
      </p>
    </div>
  </div>
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
      errorMessage: '',
      hasError: false,
      particles: Array(30).fill().map(() => ({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 5 + 3,
        color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)`,
        opacity: Math.random() * 0.5 + 0.2,
        speed: Math.random() * 0.5 + 0.2
      }))
    };
  },
  mounted() {
    this.animateParticles();
    window.addEventListener('resize', this.resetParticles);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resetParticles);
    cancelAnimationFrame(this.animationFrame);
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
    validateForm() {
      if (!this.email || !this.password) {
        this.errorMessage = 'Todos los campos son obligatorios';
        this.hasError = true;
        return false;
      }
      
      if (!this.validEmail(this.email)) {
        this.errorMessage = 'Formato de email inválido';
        this.hasError = true;
        return false;
      }
      
      this.hasError = false;
      return true;
    },
    
    validEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    
    clearError() {
      this.errorMessage = '';
      this.hasError = false;
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
            
            this.$swal({
              title: 'Inicio de sesión exitoso',
              text: `Bienvenido, ${user.name}!`,
              icon: 'success',
              confirmButtonColor: '#047ffa',
              showClass: {
                popup: 'animate__animated animate__fadeInDown'
              },
              hideClass: {
                popup: 'animate__animated animate__fadeOutUp'
              }
            }).then(() => {
              this.$router.push('/main');
            });
            
            this.errorMessage = '';
          })
          .catch(error => {
            console.error('Error al iniciar sesión:', error);
            this.errorMessage = error;
            this.hasError = true;
            
            this.$swal({
              title: 'Error al iniciar sesión',
              text: error,
              icon: 'error',
              confirmButtonColor: '#e74c3c',
              showClass: {
                popup: 'animate__animated animate__headShake'
              }
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
/* Variables CSS actualizadas */
:root {
  --color-primary: #047ffa;
  --color-primary-light: #4da8ff;
  --color-primary-dark: #0366d6;
  --color-error: #e74c3c;
  --color-error-light: #ff6b6b;
  --color-success: #2ecc71;
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
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%234da8ff'%3E%3C/path%3E%3C/svg%3E");
}

.wave-2 {
  animation: wave 10s linear infinite reverse;
  opacity: 0.3;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%234da8ff'%3E%3C/path%3E%3C/svg%3E");
}

.wave-3 {
  animation: wave 5s linear infinite;
  opacity: 0.1;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%234da8ff'%3E%3C/path%3E%3C/svg%3E");
}

@keyframes wave {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* Contenedor del login */
.login-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 5vh;
  min-height: 100vh;
}

.login-container {
  max-width: 420px;
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
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
}

.login-container.shake {
  animation: shake 0.6s;
}

/* Logo y nombre de la empresa */
.logo-container {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo {
  width: 320px;
  height: 388px;
  margin-bottom: -10rem;
  margin-top: -10rem;
}

/* Resto de estilos (se mantienen igual que en la versión anterior) */
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

.animated-form {
  animation: fadeIn 0.8s ease-out 0.2s both;
}

.input-group {
  margin-bottom: 1.8rem;
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

.error-message {
  color: var(--color-error);
  background-color: rgba(231, 76, 60, 0.1);
  padding: 12px;
  border-radius: var(--border-radius);
  margin: 1.5rem 0;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.error-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
  flex-shrink: 0;
}

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
}

.submit-button:hover {
  background: var(0 6px 8px rgba(10, 61, 112, 0.3));
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

.animated-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
  animation: fadeIn 0.8s ease-out;
}

.animated-link a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  position: relative;
  transition: color 0.3s ease;
}

.animated-link a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width 0.3s ease;
}

.animated-link a:hover {
  color: var(--color-primary-dark);
}

.animated-link a:hover::after {
  width: 100%;
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
@media (max-width: 480px) {
  .login-container {
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