import { createRouter, createWebHistory } from 'vue-router';

// Importar vistas
import HomeView from '@/views/Home/HomeView.vue'; // Nueva vista
import LoginView from '@/views/Auth/LoginView.vue';
import ProductosView from '@/views/Productos/ProductosView.vue';
import CheckoutView from '@/views/Checkout/CheckoutView.vue';
import Register from '@/views/Auth/Register.vue';
import Contraseña from '@/views/Auth/Contraseña.vue';
import MetodoPago from '@/components/MetodoPago.vue';
import DetalleProducto from '@/views/Productos/DetalleProducto.vue'; // Añadido
import CategoriasView from '@/views/Productos/CategoriasView.vue'; // Añadido

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
    path: '/productos/:id', // Ruta dinámica para el detalle del producto
    name: 'DetalleProducto',
    component: DetalleProducto 
  },
  {
    path: '/categorias', // Ruta para las categorías
    name: 'CategoriasView',
    component: CategoriasView 
  },
  { 
    path: '/checkout',
    name: 'Checkout',
    component: CheckoutView 
  },
  {
    path: '/registro', 
    name: 'Register',
    component: Register
  },
  {
    path: '/Contraseña', 
    name: 'Contraseña',
    component: Contraseña
  },
  {
    path: '/metodo-de-pago',
    name: 'metodo-de-pago',
    component: MetodoPago
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;