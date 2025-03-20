import { createRouter, createWebHistory } from 'vue-router';

// Importar vistas
import HomeView from '@/views/Home/HomeView.vue'; // Vista principal
import LoginView from '@/views/Auth/LoginView.vue'; // Vista de inicio de sesión
import ProductosView from '@/views/Productos/ProductosView.vue'; // Vista de productos
import CheckoutView from '@/views/Checkout/CheckoutView.vue'; // Vista de checkout
import DetalleProducto from '@/views/Productos/DetalleProducto.vue'; // Vista de detalle de producto
import CategoriasView from '@/views/Productos/CategoriasView.vue'; // Vista de categorías
import Register from '@/views/Auth/Register.vue'; // Vista de registro
import Contraseña from '@/views/Auth/Contraseña.vue'; // Vista de recuperación de contraseña
import MetodoPago from '@/components/MetodoPago.vue'; // Componente de método de pago

// Definir rutas
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
  }
];

// Crear el router
const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;