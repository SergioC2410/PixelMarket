<template>
    <div class="password-recovery-container">
      <!-- Paso 1: Selección de método -->
      <div v-if="currentStep === 1" class="recovery-step">
        <h2>Recuperar contraseña</h2>
        <form @submit.prevent="handleMethodSubmit">
          <div class="form-group">
            <label>Selecciona método de recuperación:</label>
            <select v-model="selectedMethod" class="method-select">
              <option value="email">Correo electrónico</option>
              <option value="phone">Número de teléfono</option>
            </select>
          </div>
  
          <div class="form-group">
            <label v-if="selectedMethod === 'email'">Ingresa tu correo:</label>
            <label v-else>Ingresa tu teléfono:</label>
            <input
              :type="selectedMethod === 'email' ? 'email' : 'tel'"
              v-model="contactInfo"
              :placeholder="selectedMethod === 'email' ? 'ejemplo@correo.com' : '+57 300 123 4567'"
              required
            >
          </div>
  
          <button type="submit" class="submit-button" :disabled="isLoading">
            {{ isLoading ? 'Enviando...' : 'Continuar' }}
          </button>
          
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </form>
      </div>
  
      <!-- Paso 2: Verificación de código -->
      <div v-if="currentStep === 2" class="recovery-step">
        <h2>Verificación de código</h2>
        <form @submit.prevent="handleCodeSubmit">
          <div class="form-group">
            <label>Ingresa el código recibido:</label>
            <input
              type="text"
              v-model.trim="verificationCode"
              placeholder="Ej: 123456"
              required
            >
          </div>
  
          <button type="submit" class="submit-button" :disabled="isLoading">
            {{ isLoading ? 'Verificando...' : 'Verificar' }}
          </button>
          
          <div class="code-actions">
            <button type="button" class="resend-button" @click="resendCode">
              Reenviar código
            </button>
          </div>
          
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </form>
      </div>
  
      <!-- Paso 3: Nueva contraseña -->
      <div v-if="currentStep === 3" class="recovery-step">
        <h2>Nueva contraseña</h2>
        <form @submit.prevent="handlePasswordSubmit">
          <div class="form-group">
            <label>Nueva contraseña:</label>
            <input
              type="password"
              v-model.trim="newPassword"
              placeholder="Mínimo 6 caracteres"
              minlength="6"
              required
            >
          </div>
  
          <div class="form-group">
            <label>Confirmar contraseña:</label>
            <input
              type="password"
              v-model.trim="confirmPassword"
              placeholder="Repite tu contraseña"
              required
            >
          </div>
  
          <button type="submit" class="submit-button" :disabled="isLoading">
            {{ isLoading ? 'Actualizando...' : 'Actualizar contraseña' }}
          </button>
          
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </form>
      </div>
  
      <!-- Paso 4: Confirmación -->
      <div v-if="currentStep === 4" class="success-message">
        <h2>¡Contraseña actualizada!</h2>
        <p>Tu contraseña ha sido cambiada exitosamente.</p>
        <router-link to="/login" class="login-link">
          Volver al inicio de sesión
        </router-link>
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
        mockCode: null // Simulación de código generado
      }
    },
    methods: {
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
        } finally {
          this.isLoading = false
        }
      },
  
      async handleCodeSubmit() {
        if (!this.verificationCode) {
          this.errorMessage = 'Ingresa el código recibido'
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
        } catch (error) {
          this.errorMessage = 'El código ingresado es incorrecto'
        } finally {
          this.isLoading = false
        }
      },
  
      async handlePasswordSubmit() {
        if (this.newPassword !== this.confirmPassword) {
          this.errorMessage = 'Las contraseñas no coinciden'
          return
        }
        
        this.isLoading = true
        
        try {
          // Simulación de actualización de contraseña - Reemplazar con API real
          await new Promise(resolve => setTimeout(resolve, 1000))
          this.currentStep = 4
        } catch (error) {
          this.errorMessage = 'Error al actualizar la contraseña'
        } finally {
          this.isLoading = false
        }
      },
  
      resendCode() {
        this.mockCode = Math.floor(100000 + Math.random() * 900000)
        console.log('Nuevo código (SIMULADO):', this.mockCode)
        alert('Se ha enviado un nuevo código')
      },
  
      validateContactInfo() {
        if (this.selectedMethod === 'email') {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          if (!emailRegex.test(this.contactInfo)) {
            this.errorMessage = 'Ingresa un correo válido'
            return false
          }
        } else {
          const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/
          if (!phoneRegex.test(this.contactInfo)) {
            this.errorMessage = 'Ingresa un número válido'
            return false
          }
        }
        return true
      }
    }
  }
  </script>
  
  <style scoped>
/* Variables - Coordinar con equipo */
.password-recovery-container {
  --color-primary: #047ffa;
  --color-error: #e74c3c;
  --border-radius: 8px;
  --transition-speed: 0.3s;
}

.password-recovery-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
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

.method-select {
  width: 100%;
  padding: 12px;
  border: 2px solid #ecf0f1;
  border-radius: var(--border-radius);
  transition: border-color var(--transition-speed) ease;
}

.method-select:focus {
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
  transition: 
    background var(--transition-speed) ease,
    opacity var(--transition-speed) ease;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.resend-button {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  margin-top: 1rem;
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

.success-message {
  text-align: center;
  color: #2ecc71;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>