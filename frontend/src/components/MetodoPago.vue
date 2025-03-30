<template>
  <!-- Componente de Métodos de Pago -->
  <div class="payment-methods">
    <!-- Título principal -->
    <h2 class="payment-title">Selecciona tu método de pago</h2>
    
    <!-- Lista de métodos de pago en acordeón -->
    <div class="accordion">
      <!-- Iteración sobre cada método de pago -->
      <div 
        v-for="method in paymentMethods" 
        :key="method.id" 
        class="accordion-item"
        :class="{ 'is-active': activeMethod === method.id }"
      >
        <!-- Encabezado del acordeón - clickeable -->
        <div 
          class="accordion-header" 
          @click="toggleAccordion(method.id)"
          :aria-expanded="!!(activeMethod === method.id)"
          :aria-controls="`method-${method.id}-content`"
        >
          <img 
            :src="method.icon" 
            :alt="`Icono ${method.name}`" 
            class="method-icon" 
            loading="lazy"
          />
          <span class="method-name">{{ method.name }}</span>
          <span class="accordion-indicator">{{ activeMethod === method.id ? '−' : '+' }}</span>
        </div>
        
        <!-- Contenido desplegable del acordeón -->
        <div 
          v-show="activeMethod === method.id" 
          class="accordion-content"
          :id="`method-${method.id}-content`"
        >
          <p class="method-description">{{ method.description }}</p>
          <button 
            @click="selectMethod(method)" 
            class="select-btn"
            aria-label="Seleccionar este método de pago"
          >
            Seleccionar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentMethods',
  data() {
    return {
      activeMethod: null, // Método activo actualmente
      paymentMethods: [
        {
          id: 1,
          name: 'Pago Móvil',
          description: 'Paga con tu banco nacional al instante.',
          icon: require('@/assets/img-pagos/vepagomovilc2c.png'),
        },
        {
          id: 2,
          name: 'Zelle',
          description: 'Paga con tu banco internacional al instante.',
          icon: require('@/assets/img-pagos/usa-zelle-c.png'),
        },
        {
          id: 3,
          name: 'Binance',
          description: 'Paga con tus USDT desde cualquier parte del mundo.',
          icon: require('@/assets/img-pagos/ven-binance.png'),
        },
        {
          id: 4,
          name: 'Efectivo',
          description: 'Paga en efectivo al momento de la entrega.',
          icon: 'https://cdn-icons-png.flaticon.com/512/1052/1052866.png',
        },
      ],
    };
  },
  methods: {
    /**
     * Alterna la visibilidad del contenido del acordeón
     * @param {number} methodId - ID del método de pago
     */
    toggleAccordion(methodId) {
      this.activeMethod = this.activeMethod === methodId ? null : methodId;
    },
    
    /**
     * Maneja la selección de un método de pago
     * @param {Object} method - Método de pago seleccionado
     */
    selectMethod(method) {
      // Emite evento para que el componente padre maneje la selección
      this.$emit('method-selected', method);
      
      // Feedback visual (opcional, podría reemplazarse por notificación)
      console.log(`Método seleccionado: ${method.name}`);
    },
  },
};
</script>

<style scoped>
/* Variables CSS para fácil mantenimiento */
:root {
  --payment-primary: #007bff;
  --payment-primary-hover: #0056b3;
  --payment-bg: #ffffff;
  --payment-border: #e0e0e0;
  --payment-text: #333333;
  --payment-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  --transition-speed: 0.3s;
  --border-radius: 10px;
}

/* Contenedor principal */
.payment-methods {
  padding: 1.5rem;
  background-color: var(--payment-bg);
  border-radius: var(--border-radius);
  max-width: 600px;
  margin: 2rem auto;
  box-shadow: var(--payment-shadow);
}

/* Título */
.payment-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  color: var(--payment-text);
  font-weight: 600;
}

/* Acordeón */
.accordion {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Elementos del acordeón */
.accordion-item {
  background-color: var(--payment-bg);
  border: 1px solid var(--payment-border);
  border-radius: var(--border-radius);
  overflow: hidden;
  transition: all var(--transition-speed) ease;
}

.accordion-item.is-active {
  border-color: var(--payment-primary);
}

/* Encabezado del acordeón */
.accordion-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  cursor: pointer;
  transition: background-color var(--transition-speed) ease;
  position: relative;
}

.accordion-header:hover {
  background-color: #f5f5f5;
}

/* Indicador de estado (+/−) */
.accordion-indicator {
  margin-left: auto;
  font-weight: bold;
  font-size: 1.2rem;
}

/* Icono del método de pago */
.method-icon {
  width: 30px;
  height: 30px;
  margin-right: 1rem;
  object-fit: contain;
}

/* Nombre del método */
.method-name {
  font-weight: 500;
  text-transform: capitalize;
}

/* Contenido del acordeón */
.accordion-content {
  padding: 1rem;
  border-top: 1px solid var(--payment-border);
  animation: fadeIn var(--transition-speed) ease;
}

/* Descripción del método */
.method-description {
  margin-bottom: 1rem;
  color: #555;
  line-height: 1.5;
}

/* Botón de selección */
.select-btn {
  display: block;
  width: 100%;
  background-color: var(--payment-primary);
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: calc(var(--border-radius) / 2);
  cursor: pointer;
  transition: background-color var(--transition-speed) ease;
  font-weight: 500;
  text-align: center;
}

.select-btn:hover {
  background-color: var(--payment-primary-hover);
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Mejoras de accesibilidad */
[aria-expanded="true"] .accordion-indicator {
  color: var(--payment-primary);
}

/* Responsive */
@media (max-width: 480px) {
  .payment-methods {
    padding: 1rem;
    margin: 1rem auto;
  }
  
  .accordion-header {
    padding: 0.75rem;
  }
}
</style>