import { createRouter, createWebHistory } from 'vue-router';

// Importar vistas
import HomeView from '@/views/Home/HomeView.vue'; // Nueva vista
import LoginView from '@/views/Auth/LoginView.vue';
import ProductosView from '@/views/Productos/ProductosView.vue';
import CheckoutView from '@/views/Checkout/CheckoutView.vue';

const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: HomeView // Ruta raíz muestra HomeView
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