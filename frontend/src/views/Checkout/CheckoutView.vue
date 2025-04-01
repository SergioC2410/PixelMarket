<template>
  <div class="checkout-container">
    <!-- Mensaje cuando no hay productos -->
    <div v-if="cartItems.length === 0" class="empty-cart-message">
      <h2>No hay productos en tu carrito</h2>
      <p>¡Explora nuestros productos y añade algunos a tu carrito!</p>
      <router-link to="/productos" class="btn btn-primary">Ver Productos</router-link>
    </div>

    <!-- Listado de productos -->
    <div class="item-list" v-if="cartItems.length > 0">
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <img :src="item.image || placeholderImage" :alt="item.name" class="product-image" />
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
            <!-- TODO: Mostrar descuento si existe -->
            <span v-if="item.discountPercentage > 0">
              Descuento: {{ item.discountPercentage }}%<br />
              Precio con Descuento en BS.F: {{ formatCurrency(calculatePriceWithDiscount(item)) }}<br />
              Precio con Descuento en Dólares: {{ formatCurrencyUSD(calculatePriceWithDiscount(item)) }}
            </span>
          </p>
          <button @click="removeItem(item)" class="remove-btn">Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Resumen de compra -->
    <div class="checkout-summary" v-if="cartItems.length > 0">
      <h2>Resumen de Pedido</h2>
      
      <!-- TODO: Mostrar detalles de envío si aplican -->
      <div v-if="shippingOptions.length > 0" class="shipping-options">
        <h3>Método de Envío</h3>
        <select v-model="selectedShipping" @change="updateShippingCost">
          <option v-for="option in shippingOptions" :key="option.id" :value="option">
            {{ option.name }} - {{ formatCurrency(option.cost) }}
          </option>
        </select>
      </div>

      <div class="summary-row">
        <span class="summary-label">Tasa de cambio:</span>
        <span class="summary-value">1 USD = {{ formatCurrency(exchangeRate) }} BS.F</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Subtotal:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(subtotal) }} | Dólares: {{ formatCurrencyUSD(subtotal) }}</span>
      </div>
      
      <!-- TODO: Mostrar descuentos si existen -->
      <div v-if="totalDiscount > 0" class="summary-row discount">
        <span class="summary-label">Descuento Total:</span>
        <span class="summary-value">- BS.F: {{ formatCurrency(totalDiscount) }} | - Dólares: {{ formatCurrencyUSD(totalDiscount) }}</span>
      </div>

      <div class="summary-row">
        <span class="summary-label">Impuestos (16%):</span>
        <span class="summary-value">BS.F: {{ formatCurrency(taxes) }} | Dólares: {{ formatCurrencyUSD(taxes) }}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Envío:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(shippingCost) }} | Dólares: {{ formatCurrencyUSD(shippingCost) }}</span>
      </div>
      <div class="summary-row total">
        <span class="summary-label">Total:</span>
        <span class="summary-value">BS.F: {{ formatCurrency(totalWithDiscount) }} | Dólares: {{ formatCurrencyUSD(totalWithDiscount) }}</span>
      </div>

      <!-- TODO: Agregar información de contacto/dirección si es necesario -->
      <div class="customer-info" v-if="!isLoggedIn">
        <h3>Información de Contacto</h3>
        <input type="email" v-model="customerEmail" placeholder="Correo electrónico" required />
        <!-- Agrega más campos según necesites -->
      </div>

      <button @click="validateCheckout" class="checkout-btn">
        Finalizar Compra
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      placeholderImage: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiB2aWV3Qm94PSIwIDAgMjQgMjQiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2RkZCIgc3Ryb2tlLXdpZHRoPSIyIj48cmVjdCB3aWR0aD0iMjAiIGhlaWdodD0iMTYiIHg9IjIiIHk9IjQiIHJ4PSIyIi8+PGNpcmNsZSBjeD0iOC41IiBjeT0iMTAuNSIgcj0iMi41Ii8+PHBhdGggZD0iTTIxIDE1bC01LjUtNS41TDEwIDE1Ii8+PC9zdmc+',
      customerEmail: '',
      selectedShipping: {},
      shippingOptions: [
        // TODO: Definir opciones de envío (puedes cargarlas desde una API)
        { id: 1, name: 'Envío Estándar', cost: 500, days: '3-5' },
        { id: 2, name: 'Envío Express', cost: 1000, days: '1-2' }
      ],
      shippingCost: 500 // Valor por defecto
    };
  },
  computed: {
    ...mapState(['cartItems', 'exchangeRate']),
    ...mapGetters(['isLoggedIn']),
    
    subtotal() {
      return this.cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    },
    taxes() {
      return this.subtotal * 0.16; // TODO: Ajustar tasa de impuestos si es necesario
    },
    total() {
      return this.subtotal + this.taxes + this.shippingCost;
    },
    totalDiscount() {
      return this.cartItems.reduce((acc, item) => {
        // TODO: Calcular descuento correctamente
        return acc + (item.discountPercentage ? (item.price * item.quantity * item.discountPercentage / 100) : 0);
      }, 0);
    },
    totalWithDiscount() {
      return this.total - this.totalDiscount;
    }
  },
  methods: {
    ...mapActions(['fetchExchangeRate', 'updateCartItem', 'removeFromCart']),
    
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
      if (!item.discountPercentage) return item.price * item.quantity;
      const discount = (item.price * item.quantity * item.discountPercentage) / 100;
      return (item.price * item.quantity) - discount;
    },
    increaseQuantity(item) {
      const newQuantity = item.quantity + 1;
      this.updateItemQuantity(item, newQuantity);
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        const newQuantity = item.quantity - 1;
        this.updateItemQuantity(item, newQuantity);
      }
    },
    validateQuantity(item) {
      if (item.quantity < 1) {
        item.quantity = 1;
        this.updateItemQuantity(item, 1);
      }
    },
    updateItemQuantity(item, newQuantity) {
      // TODO: Actualizar cantidad en el store
      this.updateCartItem({
        productId: item.id,
        quantity: newQuantity
      });
    },
    removeItem(item) {
      // TODO: Eliminar item del carrito
      this.removeFromCart(item.id);
    },
    updateShippingCost() {
      // TODO: Actualizar costo de envío según selección
      this.shippingCost = this.selectedShipping.cost || 500;
    },
    async validateCheckout() {
      if (this.cartItems.length === 0) {
        alert('No hay productos en tu carrito. Por favor, añade al menos un producto para continuar.');
        return;
      }

      // TODO: Validar información del cliente si es necesario
      if (!this.isLoggedIn && !this.customerEmail) {
        alert('Por favor ingresa tu correo electrónico para continuar.');
        return;
      }

      // TODO: Preparar datos para la orden
      const orderData = {
        items: this.cartItems.map(item => ({
          productId: item.id,
          quantity: item.quantity,
          price: item.price,
          discount: item.discountPercentage || 0
        })),
        subtotal: this.subtotal,
        taxes: this.taxes,
        shipping: this.shippingCost,
        total: this.totalWithDiscount,
        customerEmail: this.customerEmail,
        shippingMethod: this.selectedShipping.name || 'Estándar'
      };

      try {
        // TODO: Enviar orden al backend
        // const response = await axios.post('/api/orders', orderData);
        // console.log('Orden creada:', response.data);
        
        // Redirigir a método de pago
        this.$router.push({ name: 'MetodoPago', state: { orderData } });
      } catch (error) {
        console.error('Error al crear la orden:', error);
        alert('Ocurrió un error al procesar tu pedido. Por favor intenta nuevamente.');
      }
    }
  },
  mounted() {
    // TODO: Inicializar valores necesarios
    this.fetchExchangeRate();
    if (this.shippingOptions.length > 0) {
      this.selectedShipping = this.shippingOptions[0];
      this.shippingCost = this.selectedShipping.cost;
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