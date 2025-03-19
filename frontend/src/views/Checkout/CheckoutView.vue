<template>
  <div class="cart-container">
    <!-- Listado de productos -->
    <div class="item-list">
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
    <div class="checkout-summary">
      <h2>Resumen de Pedido</h2>
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
      <button @click="proceedToCheckout" class="checkout-btn">Finalizar Compra</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cartItems: [
        { id: 1, name: 'Producto A', price: 1000, quantity: 1, image: 'url', discountPercentage: 10 },
        { id: 2, name: 'Producto B', price: 2000, quantity: 2, image: 'url', discountPercentage: 5 },
      ],
      shippingCost: 500,
      taxRate: 0.16,
      exchangeRate: 100 // Ejemplo de tipo de cambio
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
    proceedToCheckout() {
      alert('Procesando el pago...');
    }
  }
};
</script>

<style scoped>
.cart-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  padding: 2rem;
  background-color: #f9f9f9;
}

.cart-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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

.remove-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.checkout-summary {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.summary-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 1rem 0;
}

.summary-label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.summary-value {
  font-size: 16px;
}

.summary-row.total {
  font-weight: bold;
}

.checkout-btn {
  width: 100%;
  padding: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.checkout-btn:hover {
  background-color: #0056b3;
}
</style>
