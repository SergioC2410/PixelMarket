import { createRouter, createWebHistory } from 'vue-router';

// Importar vistas
import LoginView from '@/views/Auth/LoginView.vue';
import ProductosView from '@/views/Productos/ProductosView.vue';
import CheckoutView from '@/views/Checkout/CheckoutView.vue';

const routes = [
  { 
    path: '/', 
    redirect: '/productos' // Redirige a productos por defecto
  },
  { 
    path: '/login',
    name: 'Login',
    component: LoginView 
  },
  { 
    path: '/productos',
    name: 'Productos',
    component: ProductosView 
  },
  { 
    path: '/checkout',
    name: 'Checkout',
    component: CheckoutView 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;