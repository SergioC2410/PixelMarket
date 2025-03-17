import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginView from '@/views/Auth/LoginView.vue'
import Register from '@/views/Auth/Register.vue'

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
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

