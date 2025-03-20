import { createRouter, createWebHistory } from 'vue-router';
// Importar vistas
import HomeView from '@/views/Home/HomeView.vue'; // Nueva vista
import LoginView from '@/views/Auth/LoginView.vue';
import ProductosView from '@/views/Productos/ProductosView.vue';
import CheckoutView from '@/views/Checkout/CheckoutView.vue';
import Register from '@/views/Auth/Register.vue';
import Contraseña from '@/views/Auth/Contraseña.vue'
import SearchResults from '@/components/SearchResults.vue';
import { createApp } from 'vue';
import App from '@/App.vue';

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
  path: '/search/:query',
  name: 'search',
  component: SearchResults,
  props: true
}
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
createApp(App).use(router).mount('#app');