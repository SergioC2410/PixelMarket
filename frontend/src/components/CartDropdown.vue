<template>
    <div class="cart-dropdown">
      <div class="cart-toggle" @click="toggleDropdown">
        <i class="fas fa-shopping-cart fa-lg"></i>
        <span v-if="cartItemCount > 0" class="cart-badge">{{ cartItemCount }}</span>
      </div>
      
      <div v-if="isOpen" class="dropdown-content" @click.stop>
        <div v-if="cartItems.length === 0" class="empty-cart">
          <i class="fas fa-shopping-cart fa-2x mb-3"></i>
          <p>Tu carrito está vacío</p>
        </div>
        
        <div v-else>
          <div v-for="item in cartItems" :key="item.id" class="cart-item">
            <img :src="item.image || require('@/assets/placeholder-product.png')" 
                 :alt="item.name" 
                 class="item-image">
            <div class="item-info">
              <h5>{{ item.name }}</h5>
              <p class="price">{{ formatCurrency(item.price * item.quantity) }}</p>
              <div class="quantity-control">
                <button @click="decreaseQuantity(item.id)" class="qty-btn">-</button>
                <span class="qty">{{ item.quantity }}</span>
                <button @click="increaseQuantity(item.id)" class="qty-btn">+</button>
              </div>
            </div>
            <button @click="removeItem(item.id)" class="remove-btn">
              <i class="fas fa-times"></i>
            </button>
          </div>
          
          <div class="cart-summary">
            <div class="summary-row">
              <span>Subtotal:</span>
              <span>{{ formatCurrency(cartTotal) }}</span>
            </div>
            <div v-if="cartTotalDiscount > 0" class="summary-row">
              <span>Descuento:</span>
              <span class="text-danger">-{{ formatCurrency(cartTotalDiscount) }}</span>
            </div>
            <div class="summary-row total">
              <span>Total:</span>
              <span class="fw-bold">{{ formatCurrency(cartTotalWithDiscount) }}</span>
            </div>
            <router-link 
              to="/checkout" 
              class="checkout-btn"
              @click.native="isOpen = false">
              Finalizar Compra
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters, mapMutations } from 'vuex';
  
  export default {
    name: 'CartDropdown',
    data() {
      return {
        isOpen: false
      };
    },
    computed: {
      ...mapGetters([
        'cartItems',
        'cartItemCount',
        'cartTotal',
        'cartTotalWithDiscount',
        'cartTotalDiscount'
      ]),
      
      formatCurrency() {
        return value => {
          return new Intl.NumberFormat('es-VE', {
            style: 'currency',
            currency: 'VES'
          }).format(value);
        };
      }
    },
    methods: {
      ...mapMutations([
        'REMOVE_FROM_CART',
        'UPDATE_CART_ITEM_QUANTITY'
      ]),
      
      toggleDropdown() {
        this.isOpen = !this.isOpen;
      },
      
      closeDropdown() {
        this.isOpen = false;
      },
      
      increaseQuantity(productId) {
        const item = this.cartItems.find(item => item.id === productId);
        if (item) {
          this.UPDATE_CART_ITEM_QUANTITY({
            productId,
            quantity: item.quantity + 1
          });
        }
      },
      
      decreaseQuantity(productId) {
        const item = this.cartItems.find(item => item.id === productId);
        if (item && item.quantity > 1) {
          this.UPDATE_CART_ITEM_QUANTITY({
            productId,
            quantity: item.quantity - 1
          });
        }
      },
      
      removeItem(productId) {
        this.REMOVE_FROM_CART(productId);
      }
    },
    mounted() {
      // Cerrar el dropdown al hacer clic fuera
      document.addEventListener('click', this.closeDropdown);
    },
    beforeDestroy() {
      document.removeEventListener('click', this.closeDropdown);
    }
  };
  </script>
 <style scoped>
 .cart-dropdown {
   position: relative;
   display: inline-block;
 }
 
 .cart-toggle {
   cursor: pointer;
   position: relative;
   display: flex;
   align-items: center;
   padding: 0.5rem;
   color: #495057;
   transition: all 0.3s ease;
   border-radius: 50%;
   width: 40px;
   height: 40px;
   justify-content: center;
 }
 
 .cart-toggle:hover {
   color: var(--color-primary);
   background-color: rgba(0, 123, 255, 0.1);
 }
 
 .cart-badge {
   position: absolute;
   top: 0;
   right: 0;
   font-size: 0.65rem;
   background-color: #dc3545;
   color: white;
   border-radius: 50%;
   width: 18px;
   height: 18px;
   display: flex;
   align-items: center;
   justify-content: center;
   font-weight: bold;
   border: 2px solid white;
 }
 
 .dropdown-content {
   position: absolute;
   right: 0;
   top: 100%;
   width: 350px;
   max-height: 70vh;
   overflow-y: auto;
   background: white;
   border: 1px solid #e9ecef;
   border-radius: 10px;
   box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
   z-index: 1050;
   padding: 20px;
   margin-top: 10px;
   transform-origin: top right;
   animation: scaleIn 0.15s ease-out forwards;
 }
 
 @keyframes scaleIn {
   from {
     opacity: 0;
     transform: scale(0.95) translateY(-10px);
   }
   to {
     opacity: 1;
     transform: scale(1) translateY(0);
   }
 }
 
 .empty-cart {
   padding: 30px 20px;
   text-align: center;
   color: #6c757d;
   display: flex;
   flex-direction: column;
   align-items: center;
 }
 
 .empty-cart i {
   color: #e9ecef;
   font-size: 2.5rem;
   margin-bottom: 15px;
 }
 
 .empty-cart p {
   margin: 0;
   font-size: 1rem;
   color: #495057;
 }
 
 .cart-items-container {
   max-height: 300px;
   overflow-y: auto;
   padding-right: 5px;
   margin-bottom: 15px;
 }
 
 /* Scrollbar styling */
 .cart-items-container::-webkit-scrollbar {
   width: 6px;
 }
 
 .cart-items-container::-webkit-scrollbar-track {
   background: #f1f1f1;
   border-radius: 10px;
 }
 
 .cart-items-container::-webkit-scrollbar-thumb {
   background: #c1c1c1;
   border-radius: 10px;
 }
 
 .cart-items-container::-webkit-scrollbar-thumb:hover {
   background: #a8a8a8;
 }
 
 .cart-item {
   display: flex;
   align-items: center;
   margin-bottom: 15px;
   padding-bottom: 15px;
   border-bottom: 1px solid #f1f1f1;
   transition: all 0.2s ease;
 }
 
 .cart-item:last-child {
   border-bottom: none;
   margin-bottom: 0;
   padding-bottom: 0;
 }
 
 .item-image {
   width: 70px;
   height: 70px;
   object-fit: cover;
   border-radius: 8px;
   margin-right: 15px;
   box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
   border: 1px solid #eee;
 }
 
 .item-info {
   flex-grow: 1;
   min-width: 0;
 }
 
 .item-info h5 {
   margin: 0 0 5px 0;
   font-size: 0.95rem;
   color: #212529;
   font-weight: 600;
   white-space: nowrap;
   overflow: hidden;
   text-overflow: ellipsis;
 }
 
 .item-info .price {
   margin: 0;
   font-weight: bold;
   color: #2c3e50;
   font-size: 0.9rem;
 }
 
 .quantity-control {
   display: flex;
   align-items: center;
   margin-top: 8px;
 }
 
 .qty-btn {
   width: 28px;
   height: 28px;
   border: 1px solid #dee2e6;
   background: #f8f9fa;
   cursor: pointer;
   border-radius: 6px;
   display: flex;
   align-items: center;
   justify-content: center;
   color: #495057;
   font-size: 0.9rem;
   transition: all 0.2s ease;
 }
 
 .qty-btn:hover {
   background: #e9ecef;
   border-color: #ced4da;
 }
 
 .qty-btn:active {
   transform: scale(0.95);
 }
 
 .qty {
   margin: 0 12px;
   min-width: 20px;
   text-align: center;
   font-weight: 500;
   font-size: 0.9rem;
 }
 
 .remove-btn {
   background: none;
   border: none;
   color: #dc3545;
   cursor: pointer;
   padding: 8px;
   font-size: 1rem;
   opacity: 0.7;
   transition: all 0.2s ease;
   margin-left: 10px;
   border-radius: 50%;
   width: 32px;
   height: 32px;
   display: flex;
   align-items: center;
   justify-content: center;
 }
 
 .remove-btn:hover {
   opacity: 1;
   background-color: rgba(220, 53, 69, 0.1);
 }
 
 .cart-summary {
   margin-top: 20px;
   padding-top: 20px;
   border-top: 1px solid #eee;
 }
 
 .summary-row {
   display: flex;
   justify-content: space-between;
   margin-bottom: 10px;
   font-size: 0.95rem;
   color: #495057;
 }
 
 .summary-row.discount {
   color: #dc3545;
 }
 
 .summary-row.total {
   font-weight: bold;
   margin: 20px 0;
   font-size: 1.1rem;
   color: #212529;
   padding-top: 10px;
   border-top: 1px dashed #ddd;
 }
 
 .checkout-btn {
   display: block;
   width: 100%;
   background: #28a745;
   color: white;
   border: none;
   padding: 12px;
   border-radius: 8px;
   text-align: center;
   text-decoration: none;
   font-weight: 600;
   transition: all 0.3s ease;
   margin-top: 15px;
   box-shadow: 0 3px 10px rgba(40, 167, 69, 0.2);
 }
 
 .checkout-btn:hover {
   background: #218838;
   transform: translateY(-2px);
   box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
 }
 
 .checkout-btn:active {
   transform: translateY(0);
 }
 
 /* Responsive styles */
 @media (max-width: 576px) {
   .dropdown-content {
     width: 300px;
     right: -20px;
   }
   
   .cart-toggle {
     padding: 0.4rem;
   }
   
   .item-image {
     width: 60px;
     height: 60px;
     margin-right: 12px;
   }
 }
 
 @media (max-width: 400px) {
   .dropdown-content {
     width: 280px;
     padding: 15px;
   }
   
   .item-info h5 {
     font-size: 0.9rem;
   }
   
   .qty-btn {
     width: 25px;
     height: 25px;
   }
   
   .qty {
     margin: 0 8px;
   }
 }
 </style> 