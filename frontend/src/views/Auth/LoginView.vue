<template>
  <!-- Contenedor principal con elementos visuales interactivos -->
  <div class="main-container">
    <!-- Fondo interactivo para ecommerce -->
    <div class="ecommerce-background"></div>
    
    <!-- Productos flotantes animados -->
    <div class="floating-products">
      <div 
        v-for="(product, index) in floatingProducts" 
        :key="'product-'+index" 
        class="floating-product" 
        :style="getProductStyle(product)"
      ></div>
    </div>
    
    <!-- Burbujas de descuento animadas -->
    <div class="discount-bubbles">
      <div 
        v-for="(bubble, index) in discountBubbles" 
        :key="'bubble-'+index" 
        class="bubble"
        :style="getBubbleStyle(bubble)"
      >
        <span>{{ bubble.text }}</span>
      </div>
    </div>
    
    <!-- Contenedor del formulario de login -->
    <div class="login-wrapper">
      <div class="login-container" :class="{ 'shake': hasError }">
        <!-- Logo de la empresa -->
        <div class="logo-container">
          <img src="@/assets/Logo/logo.png" alt="PixelMarket Logo" class="logo">
        </div>

        <h2 class="animated-title">Iniciar sesión</h2>

        <!-- Formulario de login -->
        <form @submit.prevent="handleSubmit" class="login-form animated-form">
          <!-- Campo de email -->
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

          <!-- Campo de contraseña -->
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

          <!-- Mensaje de error -->
          <transition name="slide-fade">
            <div v-if="errorMessage" class="error-message">
              <svg class="error-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
              </svg>
              {{ errorMessage }}
            </div>
          </transition>

          <!-- Botón de submit -->
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

        <!-- Enlaces adicionales -->
        <p class="register-link animated-link">
          ¿Primera vez aquí? 
          <router-link to="/registro">Crear cuenta</router-link>
        </p>

        <p class="password-link animated-link">
          ¿Olvidaste tu contraseña?
          <router-link to="/contraseña">Recuperar contraseña</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// Datos de productos para el fondo animado
const PRODUCT_IMAGES = [
  'https://static.vecteezy.com/system/resources/previews/016/283/734/non_2x/smartphone-cartoon-style-vector.jpg',
  'https://previews.123rf.com/images/larryrains/larryrains1901/larryrains190100027/118556689-laptop-una-ilustración-de-dibujos-animados-de-vector-de-una-computadora-portátil.jpg',
  'https://st4.depositphotos.com/11953928/25417/v/450/depositphotos_254173522-stock-illustration-technology-earpod-cartoon.jpg',
  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIyo9Qct5KHX947WsivC2XaC7RnY9-p3pyUw&s',
  'https://media.istockphoto.com/id/1298405700/es/vector/reloj-marrón-en-la-muñeca-símbolo-de-tiempo-aislado-sobre-fondo-blanco-ilustración.jpg?s=612x612&w=0&k=20&c=bdmaX7Z_qc9bL1YHUhgbqcpzBXU-tOywhG2buWeNMb0=',
  'https://i.pinimg.com/736x/1b/bd/c7/1bbdc7eae11e8cd58767ae3c658293ec.jpg',
  'https://img.freepik.com/vector-premium/icono-camara-dibujos-animados-diseno-plano_387795-125.jpg',
  'https://previews.123rf.com/images/pandavector/pandavector1609/pandavector160900361/63131449-pesas-de-dibujos-animados-icono-icono-del-deporte-individual-de-la-gran-aptitud-sano-recolección.jpg',
  'https://i.ebayimg.com/thumbs/images/g/m7AAAOSw5zdm0rXh/s-l1200.jpg',
  'https://i.pinimg.com/474x/26/da/00/26da0013f426665d2cd4f29b225ab99a.jpg'
];

// Textos para las burbujas de descuento
const DISCOUNT_TEXTS = ['-20%', 'Oferta', 'Nuevo', '¡Compra ya!', 'Envío gratis', '2x1'];

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      isLoading: false,
      hasError: false,
      errorMessage: '',
      animationFrame: null,
      floatingProducts: Array(10).fill().map((_, i) => this.generateProduct(i)),
      discountBubbles: Array(5).fill().map(() => this.generateBubble())
    };
  },
  methods: {
    /**
     * Genera un producto flotante con propiedades aleatorias
     * @param {number} index - Índice del producto
     * @returns {object} Objeto con las propiedades del producto
     */
    generateProduct(index) {
      return {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 80 + 40,
        rotation: Math.random() * 360,
        speed: Math.random() * 0.3 + 0.2,
        image: PRODUCT_IMAGES[index % PRODUCT_IMAGES.length],
        shadow: `rgba(4, 127, 250, ${Math.random() * 0.3 + 0.2})`
      };
    },

    /**
     * Genera una burbuja de descuento con propiedades aleatorias
     * @returns {object} Objeto con las propiedades de la burbuja
     */
    generateBubble() {
      return {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 60 + 40,
        color: `hsl(${Math.random() * 60 + 190}, 70%, 60%)`,
        opacity: Math.random() * 0.4 + 0.2,
        speed: Math.random() * 0.5 + 0.3,
        delay: Math.random() * 5,
        text: DISCOUNT_TEXTS[Math.floor(Math.random() * DISCOUNT_TEXTS.length)]
      };
    },

    /**
     * Devuelve el estilo CSS para un producto flotante
     * @param {object} product - Objeto del producto
     * @returns {object} Estilos CSS
     */
    getProductStyle(product) {
      return {
        left: `${product.x}px`,
        top: `${product.y}px`,
        width: `${product.size}px`,
        height: `${product.size}px`,
        transform: `rotate(${product.rotation}deg)`,
        backgroundImage: `url(${product.image})`,
        filter: `drop-shadow(0 5px 15px ${product.shadow})`
      };
    },

    /**
     * Devuelve el estilo CSS para una burbuja de descuento
     * @param {object} bubble - Objeto de la burbuja
     * @returns {object} Estilos CSS
     */
    getBubbleStyle(bubble) {
      return {
        left: `${bubble.x}px`,
        top: `${bubble.y}px`,
        width: `${bubble.size}px`,
        height: `${bubble.size}px`,
        backgroundColor: bubble.color,
        opacity: bubble.opacity,
        animationDelay: `${bubble.delay}s`
      };
    },

    /**
     * Maneja el envío del formulario
     */
     async handleSubmit() {
  if (!this.validateForm()) return;
  
  this.isLoading = true;
  this.clearError();

  try {
    // DEBUG: Mostrar información de la petición
    console.log('Endpoint:', this.$axios.defaults.baseURL + 'auth/login/');
    console.log('Datos enviados:', { 
      email: this.email, 
      password: '[PROTEGIDO]' // Por seguridad, no mostramos la contraseña real
    });

    const response = await this.$axios.post('auth/login/', {
      email: this.email,
      password: this.password
    });

    // DEBUG: Mostrar respuesta del servidor
    console.log('Respuesta recibida:', {
      status: response.status,
      data: response.data
    });

    // Guardar token y datos de usuario
    localStorage.setItem('access_token', response.data.access);
    
    // DEBUG: Verificar token almacenado
    console.log('Token almacenado:', localStorage.getItem('access_token'));
    
    // Redirigir al dashboard/home
    this.$router.push('/');
    
  } catch (error) {
    // DEBUG: Mostrar error detallado
    console.error('Error en la petición:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    
    this.handleLoginError(error);
  } finally {
    this.isLoading = false;
  }
},
    /**
     * Maneja errores de login
     * @param {object} error - Error de la petición
     */
    handleLoginError(error) {
      let errorMessage = 'Error al iniciar sesión';
      const defaultMessage = 'Credenciales incorrectas';
      
      if (error.response) {
        // Errores específicos del backend
        const { status, data } = error.response;
        
        switch (status) {
          case 400:
            errorMessage = data.detail || data.message || defaultMessage;
            break;
          case 401:
            errorMessage = data.detail || defaultMessage;
            break;
          case 403:
            errorMessage = 'Cuenta no verificada. Por favor verifica tu email';
            break;
          case 429:
            errorMessage = 'Demasiados intentos. Por favor espera un momento';
            break;
          case 500:
            errorMessage = 'Error del servidor. Por favor intenta más tarde';
            break;
        }
      } else if (error.request) {
        errorMessage = 'No se pudo conectar al servidor. Verifica tu conexión';
      }

      this.showError(errorMessage);
    },

    /**
     * Valida los campos del formulario
     * @returns {boolean} True si el formulario es válido
     */
    validateForm() {
      if (!this.email) {
        this.showError('Por favor ingresa tu correo electrónico');
        return false;
      }
      
      // Validación básica de email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.showError('Por favor ingresa un correo electrónico válido');
        return false;
      }
      
      if (!this.password) {
        this.showError('Por favor ingresa tu contraseña');
        return false;
      }
      
      if (this.password.length < 6) {
        this.showError('La contraseña debe tener al menos 6 caracteres');
        return false;
      }
      
      return true;
    },

    /**
     * Muestra un mensaje de error
     * @param {string} message - Mensaje de error a mostrar
     */
    showError(message) {
      this.errorMessage = message;
      this.hasError = true;
      this.isLoading = false;
    },

    /**
     * Limpia los errores del formulario
     */
    clearError() {
      this.errorMessage = '';
      this.hasError = false;
    },

    /**
     * Animación de los elementos flotantes
     */
    animateFloatingElements() {
      this.floatingProducts.forEach(product => {
        product.y += product.speed;
        product.rotation += 0.2;
        
        if (product.y > window.innerHeight) {
          product.y = -100;
          product.x = Math.random() * window.innerWidth;
        }
      });
      
      this.discountBubbles.forEach(bubble => {
        bubble.y -= bubble.speed;
        if (bubble.y < -50) {
          bubble.y = window.innerHeight + 50;
          bubble.x = Math.random() * window.innerWidth;
        }
      });
      
      this.animationFrame = requestAnimationFrame(this.animateFloatingElements);
    },

    /**
     * Reinicia las posiciones de los elementos al cambiar el tamaño de la ventana
     */
    resetPositions() {
      this.floatingProducts = this.floatingProducts.map((p) => ({
        ...p,
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      }));
      
      this.discountBubbles = this.discountBubbles.map(() => this.generateBubble());
    }
  },
  mounted() {
    // Si ya está autenticado, redirigir
    if (localStorage.getItem('access_token')) {
      this.$router.push('/');
    }
    this.animateFloatingElements();
    window.addEventListener('resize', this.resetPositions);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resetPositions);
    cancelAnimationFrame(this.animationFrame);
  }
};
</script>

<style scoped>
/* ============ VARIABLES CSS ============ */
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

/* ============ ESTILOS BASE ============ */
.main-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
}

/* ============ FONDO Y ELEMENTOS ANIMADOS ============ */
.ecommerce-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  z-index: -1;
}

.floating-products {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.floating-product {
  position: absolute;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.8;
  transition: transform 0.5s ease;
  will-change: transform;
}

.floating-product:hover {
  transform: scale(1.1) rotate(5deg);
}

.discount-bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.bubble {
  position: absolute;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 0.8em;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
  animation: float-up 15s infinite linear;
}

@keyframes float-up {
  0% { transform: translateY(0); }
  100% { transform: translateY(-100vh); }
}

/* ============ CONTENEDOR DEL LOGIN ============ */
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
  z-index: 10;
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

/* ============ LOGO ============ */
.logo-container {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo {
  width: 100px;
  height: auto;
  margin-bottom: 1rem;
}

/* ============ TÍTULO ============ */
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

/* ============ FORMULARIO ============ */
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

/* ============ ESTILOS DE ERROR ============ */
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

/* ============ TRANSICIONES ============ */
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

/* ============ BOTÓN ============ */
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
  background: var(--color-primary-dark);
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

/* ============ ENLACES ============ */
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

/* ============ ANIMACIONES ============ */
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

/* ============ RESPONSIVE ============ */
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
  
  .logo {
    width: 80px;
  }
}
</style>