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

  <!-- Contenedor de métodos de pago -->
  <div class="payment-methods-wrapper">
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
      
      // Elementos del fondo interactivo
      floatingProducts: Array(10).fill().map((_, i) => ({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: Math.random() * 80 + 40,
        rotation: Math.random() * 360,
        speed: Math.random() * 0.3 + 0.2,
        image: this.getRandomProductImage(i),
        shadow: `rgba(74, 107, 255, ${Math.random() * 0.3 + 0.2})`
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
    };
  },
  methods: {
    toggleAccordion(methodId) {
      this.activeMethod = this.activeMethod === methodId ? null : methodId;
    },
    selectMethod(method) {
      this.$emit('method-selected', method);
    },
    
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
      const discounts = ['-20%', 'Oferta', 'Nuevo', '¡Paga fácil!', 'Descuento', 'Promo'];
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

/* Fondo interactivo */
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
.payment-methods-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.payment-methods {
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius);
  max-width: 600px;
  margin: 2rem auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  transition: all var(--transition-speed) ease;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 100%;
}

.payment-methods:hover {
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

/* Título */
.payment-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  color: var(--payment-text);
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  background-color: rgba(255, 255, 255, 0.8);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  display: inline-block;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

/* Acordeón */
.accordion {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Elementos del acordeón */
.accordion-item {
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--payment-border);
  border-radius: var(--border-radius);
  overflow: hidden;
  transition: all var(--transition-speed) ease;
  box-shadow: var(--payment-shadow);
  backdrop-filter: blur(2px);
}

.accordion-item:hover {
  box-shadow: var(--payment-shadow-hover);
  transform: translateY(-2px);
}

.accordion-item.is-active {
  border-color: var(--payment-primary);
  box-shadow: var(--payment-shadow-active);
  background-color: rgba(240, 244, 255, 0.95);
}

/* Encabezado del acordeón */
.accordion-header {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  position: relative;
  background-color: transparent;
}

.accordion-header:hover {
  background-color: rgba(248, 249, 250, 0.7);
}

.accordion-item.is-active .accordion-header {
  background-color: rgba(240, 244, 255, 0.95);
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
  background-color: rgba(248, 249, 250, 0.9);
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
    font-size: 1.4rem;
    padding: 0.5rem;
  }
  
  .method-icon {
    width: 30px;
    height: 30px;
  }
  
  .select-btn {
    padding: 0.75rem;
    font-size: 0.9rem;
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