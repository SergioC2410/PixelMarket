<template>
  <div class="cart-container">
    <!-- Mensaje cuando no hay productos -->
    <div v-if="cartItems.length === 0" class="empty-cart-message">
      <h2>No hay productos en tu carrito</h2>
      <p>¡Explora nuestros productos y añade algunos a tu carrito!</p>
    </div>

    <!-- Listado de productos -->
    <div class="item-list" v-if="cartItems.length > 0">
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <img :src="item.image" :alt="item.name" class="product-image" />
        <div class="item-details">
          <h3>{{ item.name }}</h3>
          <div class="quantity-controls">
            <button @click="decreaseQuantity(item)" class="quantity-btn">-</button>
            <input 
              type="number" 
              v-model.number="item.quantity" 
              min="1"
              @change="validateQuantity(item)"
            />
            <button @click="increaseQuantity(item)" class="quantity-btn">+</button>
          </div>
          <p>
            Precio en BS.F: {{ formatCurrency(item.price * item.quantity) }}<br />
            Precio en Dólares: {{ formatCurrencyUSD(item.price * item.quantity) }}<br />
            Descuento: {{ item.discountPercentage }}%<br />
            Precio con Descuento en BS.F: {{ formatCurrency(calculatePriceWithDiscount(item)) }}<br />
            Precio con Descuento en Dólares: {{ formatCurrencyUSD(calculatePriceWithDiscount(item)) }}
          </p>
          <button @click="removeItem(item)" class="remove-btn">Eliminar</button>
        </div>
      </div>
    </div>
    <!-- Resumen de compra -->
    <div class="checkout-summary" v-if="cartItems.length > 0">
      <h2>Resumen de Pedido</h2>
      <div class="summary-row">
        <span class="summary-label">Tasa de cambio:</span>
        <span class="summary-value">1 USD = {{ formatCurrency(exchangeRate) }} BS.F</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Subtotal:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(subtotal) }} | Dólares: {{ formatCurrencyUSD(subtotal) }}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Impuestos (16%):</span>
        <span class="summary-value">BS.F: {{ formatCurrency(taxes) }} | Dólares: {{ formatCurrencyUSD(taxes) }}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Envío:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(shippingCost) }} | Dólares: {{ formatCurrencyUSD(shippingCost) }}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Descuento Total:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(totalDiscount) }} | Dólares: {{ formatCurrencyUSD(totalDiscount) }}</span>
      </div>
      <div class="summary-row total">
        <span class="summary-label">Total:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(totalWithDiscount) }} | Dólares: {{ formatCurrencyUSD(totalWithDiscount) }}</span>
      </div>
      <button @click="validateCheckout" class="checkout-btn">
        Finalizar Compra
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      cartItems: [], // Inicializamos vacío para probar el mensaje
      shippingCost: 500,
      taxRate: 0.16,
      exchangeRate: 1, // Inicializamos en 1, se actualizará con la API
    };
  },
  computed: {
    subtotal() {
      return this.cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    },
    taxes() {
      return this.subtotal * this.taxRate;
    },
    total() {
      return this.subtotal + this.taxes + this.shippingCost;
    },
    totalDiscount() {
      return this.cartItems.reduce((acc, item) => acc + this.calculateDiscount(item), 0);
    },
    totalWithDiscount() {
      return this.total - this.totalDiscount;
    }
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('es-VE', {
        style: 'decimal',
        minimumFractionDigits: 2
      }).format(value);
    },
    formatCurrencyUSD(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value / this.exchangeRate);
    },
    calculatePriceWithDiscount(item) {
      const discount = (item.price * item.quantity * item.discountPercentage) / 100;
      return (item.price * item.quantity) - discount;
    },
    calculateDiscount(item) {
      return (item.price * item.quantity * item.discountPercentage) / 100;
    },
    increaseQuantity(item) {
      item.quantity++;
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) item.quantity--;
    },
    validateQuantity(item) {
      if (item.quantity < 1) item.quantity = 1;
    },
    removeItem(item) {
      this.cartItems = this.cartItems.filter(i => i.id !== item.id);
    },
    validateCheckout() {
      if (this.cartItems.length === 0) {
        alert('No hay productos en tu carrito. Por favor, añade al menos un producto para continuar.');
        return;
      }
      this.$router.push({ name: 'MetodoPago' });
    },
    async fetchExchangeRate() {
      try {
        const apiKey = '486f0d2b81e7c30a7340fb24'; // Tu clave API de ExchangeRate-API
        const response = await axios.get(`https://v6.exchangerate-api.com/v6/${apiKey}/latest/USD`);
        this.exchangeRate = response.data.conversion_rates.VES; // Obtener la tasa de cambio USD a VES
      } catch (error) {
        console.error('Error al obtener el tipo de cambio:', error);
        this.exchangeRate = 66.78; // Valor por defecto en caso de error
      }
    }
  },
  mounted() {
    this.fetchExchangeRate(); // Llamar a la API al cargar el componente
    
    // Para probar el mensaje de carrito vacío, dejamos cartItems vacío
    // Si quieres ver el carrito con productos, descomenta las siguientes líneas:
    
    this.cartItems = [
      { 
        id: 1, 
        name: 'Producto A', 
        price: 1000, 
        quantity: 1, 
        image: 'https://via.placeholder.com/120',
        discountPercentage: 10 
      },
      { 
        id: 2, 
        name: 'Producto B', 
        price: 2000, 
        quantity: 2, 
        image: 'https://via.placeholder.com/120?text=Producto+B', 
        discountPercentage: 5 
      }
    ];
    
  }
};
</script>

<style scoped>
.cart-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  padding: 2rem;
  background-color: #f0f8ff;
  min-height: 70vh;
  position: relative;
}

.empty-cart-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
}

.empty-cart-message h2 {
  font-size: 2rem;
  color: #666;
  margin-bottom: 1rem;
}

.empty-cart-message p {
  font-size: 1.2rem;
  color: #888;
}

.cart-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid #ffff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #ffff;
}

.product-image {
  width: 120px;
  height: 120px;
  object-fit: contain;
  border-radius: 8px;
}

.item-details {
  flex-grow: 1;
}

.quantity-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 1rem;
}

.quantity-controls input {
  width: 50px;
  height: 30px;
  font-size: 16px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  font-size: 18px;
  font-weight: bold;
  border: none;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
.quantity-btn:hover {
  background-color: #0056b3;}

.remove-btn {
  background-color: #f50820;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.remove-btn:hover {
  background-color: #ca0b1e;
}

.checkout-summary {
  background-color: #ffff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin: 1rem 0;
}

.summary-label {
  font-weight: bold;
}

.summary-value {
  font-size: 16px;
}

.summary-row.total {
  font-weight: bold;
}

.checkout-btn {
  width: 100%;
  padding: 3%;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration-line: none;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
}

.checkout-btn:hover {
  background-color: #0056b3;
}

.checkout-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>