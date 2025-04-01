<template>
  <!-- Fondo interactivo para ecommerce -->
  <div class="ecommerce-background">
    <!-- Productos flotantes -->
    <div class="floating-products">
      <div v-for="(product, index) in floatingProducts" :key="'product-'+index" class="floating-product" 
           :style="{
             left: product.x + 'px',
             top: product.y + 'px',
             width: product.size + 'px',
             height: product.size + 'px',
             transform: 'rotate(' + product.rotation + 'deg)',
             backgroundImage: 'url(' + product.image + ')',
             filter: 'drop-shadow(0 5px 15px ' + product.shadow + ')'
           }"></div>
    </div>
    
    <!-- Efecto de burbujas de descuento -->
    <div class="discount-bubbles">
      <div v-for="(bubble, index) in discountBubbles" :key="'bubble-'+index" class="bubble" 
           :style="{
             left: bubble.x + 'px',
             top: bubble.y + 'px',
             width: bubble.size + 'px',
             height: bubble.size + 'px',
             backgroundColor: bubble.color,
             opacity: bubble.opacity,
             animationDelay: bubble.delay + 's'
           }">
        <span>{{ bubble.text }}</span>
      </div>
    </div>
  </div>

  <!-- Contenedor de recuperación de contraseña -->
  <div class="password-recovery-wrapper">
    <div class="password-recovery-container" :class="{ 'shake': hasError }">
      <!-- Paso 1: Selección de método -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="currentStep === 1" class="recovery-step animated-step">
          <h2 class="animated-title">Recuperar contraseña</h2>
          <form @submit.prevent="handleMethodSubmit" class="animated-form">
            <div class="form-group" :class="{ 'input-error': hasError }">
              <label for="recovery-method">Selecciona método de recuperación:</label>
              <select 
                id="recovery-method"
                v-model="selectedMethod" 
                class="method-select animated-input"
                @change="clearError"
              >
                <option value="email">Correo electrónico</option>
                <option value="phone">Número de teléfono</option>
              </select>
              <span class="input-focus-border"></span>
            </div>

            <div class="form-group" :class="{ 'input-error': hasError }">
              <label 
                v-if="selectedMethod === 'email'" 
                for="contact-info"
              >
                Ingresa tu correo:
              </label>
              <label 
                v-else 
                for="contact-info"
              >
                Ingresa tu teléfono:
              </label>
              <input
                id="contact-info"
                :type="selectedMethod === 'email' ? 'email' : 'tel'"
                v-model="contactInfo"
                :placeholder="selectedMethod === 'email' ? 'ejemplo@correo.com' : '+58 123 456 78 90'"
                required
                class="animated-input"
                @input="clearError"
              >
              <span class="input-focus-border"></span>
            </div>

            <button 
              type="submit" 
              class="submit-button"
              :disabled="isLoading"
              :class="{ loading: isLoading }"
              @mousedown="pulse = true"
              @mouseup="pulse = false"
              @mouseleave="pulse = false"
              :style="{ transform: pulse ? 'scale(0.98)' : 'scale(1)' }"
            >
              <span class="button-content">
                <svg class="button-icon" viewBox="0 0 24 24" v-if="!isLoading">
                  <path fill="currentColor" d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z" />
                </svg>
                <svg class="spinner" viewBox="0 0 50 50" v-else>
                  <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                </svg>
                <span>{{ isLoading ? 'Enviando...' : 'Continuar' }}</span>
              </span>
            </button>
            
            <transition name="slide-fade">
              <div v-if="errorMessage" class="error-message">
                <svg class="error-icon" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
                </svg>
                {{ errorMessage }}
              </div>
            </transition>
          </form>
        </div>

        <!-- Paso 2: Verificación de código -->
        <div v-else-if="currentStep === 2" class="recovery-step animated-step">
          <h2 class="animated-title">Verificación de código</h2>
          <form @submit.prevent="handleCodeSubmit" class="animated-form">
            <div class="form-group" :class="{ 'input-error': hasError }">
              <label for="verification-code">Ingresa el código recibido:</label>
              <input
                id="verification-code"
                type="text"
                v-model.trim="verificationCode"
                placeholder="Ej: 123456"
                required
                class="animated-input"
                @input="clearError"
              >
              <span class="input-focus-border"></span>
            </div>

            <button 
              type="submit" 
              class="submit-button"
              :disabled="isLoading"
              :class="{ loading: isLoading }"
              @mousedown="pulse = true"
              @mouseup="pulse = false"
              @mouseleave="pulse = false"
              :style="{ transform: pulse ? 'scale(0.98)' : 'scale(1)' }"
            >
              <span class="button-content">
                <svg class="button-icon" viewBox="0 0 24 24" v-if="!isLoading">
                  <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                </svg>
                <svg class="spinner" viewBox="0 0 50 50" v-else>
                  <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                </svg>
                <span>{{ isLoading ? 'Verificando...' : 'Verificar' }}</span>
              </span>
            </button>
            
            <div class="code-actions">
              <button 
                type="button" 
                class="resend-button"
                @click="resendCode"
                :disabled="isResending"
              >
                <span v-if="!isResending">Reenviar código</span>
                <span v-else>Enviando...</span>
              </button>
            </div>
            
            <transition name="slide-fade">
              <div v-if="errorMessage" class="error-message">
                <svg class="error-icon" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
                </svg>
                {{ errorMessage }}
              </div>
            </transition>
          </form>
        </div>

        <!-- Paso 3: Nueva contraseña -->
        <div v-else-if="currentStep === 3" class="recovery-step animated-step">
          <h2 class="animated-title">Nueva contraseña</h2>
          <form @submit.prevent="handlePasswordSubmit" class="animated-form">
            <div class="form-group" :class="{ 'input-error': hasError }">
              <label for="new-password">Nueva contraseña:</label>
              <input
                id="new-password"
                type="password"
                v-model.trim="newPassword"
                placeholder="Mínimo 6 caracteres"
                minlength="6"
                required
                class="animated-input"
                @input="clearError"
              >
              <span class="input-focus-border"></span>
            </div>

            <div class="form-group" :class="{ 'input-error': hasError }">
              <label for="confirm-password">Confirmar contraseña:</label>
              <input
                id="confirm-password"
                type="password"
                v-model.trim="confirmPassword"
                placeholder="Repite tu contraseña"
                required
                class="animated-input"
                @input="clearError"
              >
              <span class="input-focus-border"></span>
            </div>

            <button 
              type="submit" 
              class="submit-button"
              :disabled="isLoading"
              :class="{ loading: isLoading }"
              @mousedown="pulse = true"
              @mouseup="pulse = false"
              @mouseleave="pulse = false"
              :style="{ transform: pulse ? 'scale(0.98)' : 'scale(1)' }"
            >
              <span class="button-content">
                <svg class="button-icon" viewBox="0 0 24 24" v-if="!isLoading">
                  <path fill="currentColor" d="M17,3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3M19,19H5V5H16.17L19,7.83V19M12,12A4,4 0 0,0 8,16A4,4 0 0,0 12,20A4,4 0 0,0 16,16A4,4 0 0,0 12,12M12,18A2,2 0 0,1 10,16A2,2 0 0,1 12,14A2,2 0 0,1 14,16A2,2 0 0,1 12,18Z" />
                </svg>
                <svg class="spinner" viewBox="0 0 50 50" v-else>
                  <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                </svg>
                <span>{{ isLoading ? 'Actualizando...' : 'Actualizar contraseña' }}</span>
              </span>
            </button>
            
            <transition name="slide-fade">
              <div v-if="errorMessage" class="error-message">
                <svg class="error-icon" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z" />
                </svg>
                {{ errorMessage }}
              </div>
            </transition>
          </form>
        </div>

        <!-- Paso 4: Confirmación -->
        <div v-else-if="currentStep === 4" class="success-message">
          <svg class="success-icon" viewBox="0 0 24 24">
            <path fill="#2ecc71" d="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" />
          </svg>
          <h2 class="animated-title">¡Contraseña actualizada!</h2>
          <p>Tu contraseña ha sido cambiada exitosamente.</p>
          <router-link to="/login" class="login-link animated-link">
            Volver al inicio de sesión
          </router-link>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordRecovery',
  data() {
    return {
      currentStep: 1,
      selectedMethod: 'email',
      contactInfo: '',
      verificationCode: '',
      newPassword: '',
      confirmPassword: '',
      errorMessage: '',
      isLoading: false,
      isResending: false,
      hasError: false,
      pulse: false,
      mockCode: null, // Simulación de código generado
      
      // Elementos del fondo interactivo
      floatingProducts: Array(10).fill().map((_, i) => ({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 80 + 40,
        rotation: Math.random() * 360,
        speed: Math.random() * 0.3 + 0.2,
        image: this.getRandomProductImage(i),
        shadow: `rgba(4, 127, 250, ${Math.random() * 0.3 + 0.2})`
      })),
      discountBubbles: Array(5).fill().map(() => ({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 60 + 40,
        color: `hsl(${Math.random() * 60 + 190}, 70%, 60%)`,
        opacity: Math.random() * 0.4 + 0.2,
        speed: Math.random() * 0.5 + 0.3,
        delay: Math.random() * 5,
        text: this.getRandomDiscountText()
      }))
    }
  },
  methods: {
    // Métodos para el fondo interactivo
    getRandomProductImage(index) {
      const products = [
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
      return products[index % products.length];
    },
    
    getRandomDiscountText() {
      const discounts = ['-20%', 'Oferta', 'Nuevo', '¡Recupérala!', 'Descuento', 'Promo'];
      return discounts[Math.floor(Math.random() * discounts.length)];
    },
    
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
    
    resetPositions() {
      this.floatingProducts = this.floatingProducts.map(product => ({
        ...product,
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      }));
      
      this.discountBubbles = this.discountBubbles.map(bubble => ({
        ...bubble,
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      }));
    },
    
    // Métodos existentes de recuperación de contraseña
    clearError() {
      this.errorMessage = '';
      this.hasError = false;
    },
    
    async handleMethodSubmit() {
      if (!this.validateContactInfo()) return
      
      this.isLoading = true
      this.errorMessage = ''
      
      try {
        // Simulación de API - Reemplazar con llamada real
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // Generar código de 6 dígitos para la demo
        this.mockCode = Math.floor(100000 + Math.random() * 900000)
        console.log('Código de verificación (SIMULADO):', this.mockCode)
        
        this.currentStep = 2
      } catch (error) {
        this.errorMessage = 'Error al enviar el código. Intenta nuevamente.'
        this.hasError = true
      } finally {
        this.isLoading = false
      }
    },

    async handleCodeSubmit() {
      if (!this.verificationCode) {
        this.errorMessage = 'Ingresa el código recibido'
        this.hasError = true
        return
      }
      
      this.isLoading = true
      
      try {
        // Simulación de verificación de código - Reemplazar con API real
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        if (parseInt(this.verificationCode) !== this.mockCode) {
          throw new Error('Código inválido')
        }
        
        this.currentStep = 3
        this.errorMessage = ''
        this.hasError = false
      } catch (error) {
        this.errorMessage = 'El código ingresado es incorrecto'
        this.hasError = true
      } finally {
        this.isLoading = false
      }
    },

    async handlePasswordSubmit() {
      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = 'Las contraseñas no coinciden'
        this.hasError = true
        return
      }
      
      this.isLoading = true
      
      try {
        // Simulación de actualización de contraseña - Reemplazar con API real
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.currentStep = 4
      } catch (error) {
        this.errorMessage = 'Error al actualizar la contraseña'
        this.hasError = true
      } finally {
        this.isLoading = false
      }
    },

    async resendCode() {
      this.isResending = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.mockCode = Math.floor(100000 + Math.random() * 900000)
        console.log('Nuevo código (SIMULADO):', this.mockCode)
        
        this.$swal({
          title: 'Código reenviado',
          text: 'Se ha enviado un nuevo código de verificación',
          icon: 'success',
          confirmButtonColor: '#047ffa',
          showClass: {
            popup: 'animate__animated animate__fadeInDown'
          }
        })
      } catch (error) {
        this.errorMessage = 'Error al reenviar el código'
        this.hasError = true
      } finally {
        this.isResending = false
      }
    },

    validateContactInfo() {
      if (this.selectedMethod === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(this.contactInfo)) {
          this.errorMessage = 'Ingresa un correo válido'
          this.hasError = true
          return false
        }
      } else {
        const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/
        if (!phoneRegex.test(this.contactInfo)) {
          this.errorMessage = 'Ingresa un número válido'
          this.hasError = true
          return false
        }
      }
      return true
    }
  },
  mounted() {
    this.animateFloatingElements();
    window.addEventListener('resize', this.resetPositions);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resetPositions);
    cancelAnimationFrame(this.animationFrame);
  }
}
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

/* Fondo para ecommerce */
.ecommerce-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  z-index: -1;
  overflow: hidden;
}

/* Productos flotantes */
.floating-products {
  position: absolute;
  width: 100%;
  height: 100%;
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

/* Burbujas de descuento */
.discount-bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
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
  cursor: pointer;
}

@keyframes float-up {
  0% { transform: translateY(0); }
  100% { transform: translateY(-100vh); }
}

/* Contenedor principal */
.password-recovery-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.password-recovery-container {
  max-width: 420px;
  width: 100%;
  padding: 2.5rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s var(--transition-easing);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.password-recovery-container.shake {
  animation: shake 0.6s;
}

.password-recovery-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
}

/* Animaciones clave */
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

/* Formulario animado */
.animated-form {
  animation: fadeIn 0.8s ease-out 0.2s both;
}

/* Grupos de entrada */
.form-group {
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

/* Campos de entrada animados */
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

.method-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 1em;
}

/* Borde animado para el foco */
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

/* Estilos para errores */
.input-error .animated-input,
.input-error .method-select {
  border-color: var(--color-error);
}

.input-error .animated-input:focus,
.input-error .method-select:focus {
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.2);
}

.input-error .input-focus-border {
  background-color: var(--color-error);
}

/* Mensaje de error */
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

/* Transiciones para mensajes */
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

/* Botón consistente */
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
  background: var(0 6px 8px rgba(4, 43, 82, 0.3));
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

/* Spinner de carga */
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

/* Botón reenviar código */
.code-actions {
  text-align: center;
  margin-top: 1rem;
}

.resend-button {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color var(--transition-speed) ease;
  padding: 0.5rem;
  position: relative;
}

.resend-button:hover {
  color: var(--color-primary-dark);
}

.resend-button:disabled {
  color: #95a5a6;
  cursor: not-allowed;
}

.resend-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width var(--transition-speed) ease;
}

.resend-button:hover::after {
  width: 100%;
}

/* Mensaje de éxito */
.success-message {
  text-align: center;
  padding: 2rem 0;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 1.5rem;
  animation: fadeIn 0.8s ease-out;
}

.success-message p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
}

/* Enlace animado */
.animated-link {
  display: inline-block;
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  position: relative;
  transition: color 0.3s ease;
  animation: fadeIn 0.8s ease-out;
}

.animated-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width 0.3s ease;
}

.animated-link:hover {
  color: var(--color-primary-dark);
}

.animated-link:hover::after {
  width: 100%;
}

/* Transiciones entre pasos */
.fade-slide-enter-active {
  transition: all 0.5s ease;
}

.fade-slide-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Responsive */
@media (max-width: 480px) {
  .password-recovery-container {
    padding: 1.5rem;
  }
  
  .animated-input, .method-select {
    padding: 12px 10px;
  }
  
  .submit-button {
    padding: 14px;
  }

  /* Reducir elementos en móviles */
  .floating-product {
    display: none;
  }
  
  .bubble {
    display: none;
  }
}
</style>