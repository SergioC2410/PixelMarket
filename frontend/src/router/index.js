import { createRouter, createWebHistory } from 'vue-router';

// Importar vistas
import HomeView from '@/views/Home/HomeView.vue';
import LoginView from '@/views/Auth/LoginView.vue';
import ProductosView from '@/views/Productos/ProductosView.vue';
import CheckoutView from '@/views/Checkout/CheckoutView.vue';
import DetalleProducto from '@/views/Productos/DetalleProducto.vue';
import CategoriasView from '@/views/Productos/CategoriasView.vue';
import Register from '@/views/Auth/Register.vue';
import Contraseña from '@/views/Auth/Contraseña.vue';
import MetodoPago from '@/components/MetodoPago.vue';
import SearchResults from '@/components/SearchResults.vue';
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"></link>
// Definir rutas
const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: HomeView
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
    path: '/productos/:id',
    name: 'DetalleProducto',
    component: DetalleProducto
  },
  {
    path: '/categorias',
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
    path: '/contraseña', 
    name: 'Contraseña',
    component: Contraseña
  },
  {
    path: '/metodo-de-pago',
    name: 'MetodoPago',
    component: MetodoPago
  },
  {
    path: '/search/:query',
    name: 'search',
    component: SearchResults,
    props: true
  }
];

// Crear el router
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
