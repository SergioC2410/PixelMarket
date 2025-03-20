import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home/Home.vue'; // 
import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginView from '@/views/Auth/LoginView.vue'
import Register from '@/views/Auth/Register.vue'
import SearchResults from '@/components/SearchResults.vue';
import { createApp } from 'vue';
import App from '@/App.vue';

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/registro', 
    name: 'Register',
    component: Register
  },
{
  path: '/search/:query',
  name: 'search',
  component: SearchResults,
  props: true
},
{
  path: '/',
  name: 'Home',
  component: Home
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router
createApp(App).use(router).mount('#app');