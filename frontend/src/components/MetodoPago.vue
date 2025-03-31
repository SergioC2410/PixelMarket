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
          aria-expanded="activeMethod === method.id"
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
        <transition name="slide-fade">
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
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentMethods',
  data() {
    return {
      activeMethod: null,
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
    toggleAccordion(methodId) {
      this.activeMethod = this.activeMethod === methodId ? null : methodId;
    },
    selectMethod(method) {
      this.$emit('method-selected', method);
    },
  },
};
</script>

<style scoped>
/* Variables CSS */
:root {
  --payment-primary: #4a6bff;
  --payment-primary-hover: #3a56d4;
  --payment-bg: #ffffff;
  --payment-border: #e0e0e0;
  --payment-text: #2d3748;
  --payment-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --payment-shadow-hover: 0 10px 15px rgba(0, 0, 0, 0.1);
  --payment-shadow-active: 0 4px 6px rgba(74, 107, 255, 0.2);
  --transition-speed: 0.3s;
  --border-radius: 12px;
}

/* Contenedor principal */
.payment-methods {
  padding: 2rem;
  background-color: #ffffff;
  border-radius: var(--border-radius);
  max-width: 600px;
  margin: 2rem auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  transition: all var(--transition-speed) ease;
}

.payment-methods:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* Título */
.payment-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  color: var(--payment-text);
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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
  box-shadow: var(--payment-shadow);
}

.accordion-item:hover {
  box-shadow: var(--payment-shadow-hover);
  transform: translateY(-2px);
}

.accordion-item.is-active {
  border-color: var(--payment-primary);
  box-shadow: var(--payment-shadow-active);
}

/* Encabezado del acordeón */
.accordion-header {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  position: relative;
  background-color: var(--payment-bg);
}

.accordion-header:hover {
  background-color: #f8f9fa;
}

.accordion-item.is-active .accordion-header {
  background-color: #f0f4ff;
}

/* Indicador de estado (+/−) */
.accordion-indicator {
  margin-left: auto;
  font-weight: bold;
  font-size: 1.2rem;
  color: #718096;
  transition: all var(--transition-speed) ease;
}

.accordion-item.is-active .accordion-indicator {
  color: var(--payment-primary);
  transform: rotate(180deg);
}

/* Icono del método de pago */
.method-icon {
  width: 36px;
  height: 36px;
  margin-right: 1rem;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: all var(--transition-speed) ease;
}

.accordion-item.is-active .method-icon {
  filter: drop-shadow(0 2px 4px rgba(74, 107, 255, 0.2));
}

/* Nombre del método */
.method-name {
  font-weight: 600;
  text-transform: capitalize;
  color: var(--payment-text);
  transition: all var(--transition-speed) ease;
}

.accordion-item.is-active .method-name {
  color: var(--payment-primary);
}

/* Contenido del acordeón */
.accordion-content {
  padding: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  background-color: #f8f9fa;
}

/* Descripción del método */
.method-description {
  margin-bottom: 1.5rem;
  color: #4a5568;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Botón de selección */
.select-btn {
  display: block;
  width: 100%;
  background-color: var(--payment-primary);
  color: white;
  border: none;
  padding: 0.85rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  font-weight: 600;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.select-btn:hover {
  background-color: var(--payment-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.select-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Animaciones */
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

/* Efecto de elevación al pasar el mouse */
.hover-lift {
  transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .payment-methods {
    padding: 1.5rem;
    margin: 1.5rem auto;
  }
  
  .payment-title {
    font-size: 1.5rem;
  }
  
  .accordion-header {
    padding: 1rem;
  }
  
  .accordion-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .payment-methods {
    padding: 1rem;
    margin: 1rem auto;
    border-radius: 8px;
  }
  
  .payment-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  color: var(--payment-text);
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* Nueva propiedad para sombra permanente */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  display: inline-block;
  background-color: var(--payment-bg);
  /* Centrar el título con sombra */
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
  
  .method-icon {
    width: 30px;
    height: 30px;
  }
  
  .select-btn {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
}
</style>