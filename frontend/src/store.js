import { createStore } from 'vuex';

export default createStore({
  state: {
    productos: [], // Estado global para los productos
    categorias: [], // Estado global para las categorías
    cargando: false, // Estado para indicar si se están cargando los productos
  },
  mutations: {
    SET_PRODUCTOS(state, productos) {
      state.productos = productos;
    },
    SET_CATEGORIAS(state, categorias) {
      state.categorias = categorias;
    },
    SET_CARGANDO(state, cargando) {
      state.cargando = cargando;
    },
  },
  actions: {
    async cargarProductos({ commit }) {
      commit('SET_CARGANDO', true); // Indicar que se están cargando los productos

      // Simulación de una llamada a una API
      setTimeout(() => {
        const productos = [
          { id: 1, nombre: 'Smartphone X', precio: 599.99, categoria: 'electrónica' },
          { id: 2, nombre: 'Laptop Pro', precio: 1299.99, categoria: 'electrónica' },
          { id: 3, nombre: 'Sofá Moderno', precio: 899.99, categoria: 'hogar' },
          { id: 4, nombre: 'Lámpara de Mesa', precio: 49.99, categoria: 'hogar' },
          { id: 5, nombre: 'Zapatos Deportivos', precio: 79.99, categoria: 'moda' },
          { id: 6, nombre: 'Chaqueta de Cuero', precio: 199.99, categoria: 'moda' },
          { id: 7, nombre: 'Balón de Fútbol', precio: 29.99, categoria: 'deportes' },
          { id: 8, nombre: 'Raqueta de Tenis', precio: 89.99, categoria: 'deportes' },
          { id: 9, nombre: 'Lego Classic', precio: 39.99, categoria: 'juguetes' },
          { id: 10, nombre: 'Muñeca Barbie', precio: 19.99, categoria: 'juguetes' },
          { id: 11, nombre: 'Cien Años de Soledad', precio: 14.99, categoria: 'libros' },
          { id: 12, nombre: 'El Principito', precio: 9.99, categoria: 'libros' },
          { id: 13, nombre: 'Kit de Maquillaje', precio: 49.99, categoria: 'belleza' },
          { id: 14, nombre: 'Crema Hidratante', precio: 24.99, categoria: 'belleza' },
          { id: 15, nombre: 'Neumáticos All-Season', precio: 199.99, categoria: 'automóviles' },
          { id: 16, nombre: 'Aceite de Motor', precio: 29.99, categoria: 'automóviles' },
        ];

        commit('SET_PRODUCTOS', productos); // Actualizar el estado con los productos
        commit('SET_CARGANDO', false); // Indicar que la carga ha terminado
      }, 1000); // Simular un retardo de 1 segundo
    },
    
    async cargarCategorias({ commit }) {
      // Simulación de una llamada a una API para cargar categorías
      setTimeout(() => {
        const categorias = [
          { id: 1, nombre: 'Electrónica', productos: 45 },
          { id: 2, nombre: 'Hogar', productos: 32 },
          { id: 3, nombre: 'Moda', productos: 78 },
          { id: 4, nombre: 'Deportes', productos: 56 },
          { id: 5, nombre: 'Juguetes', productos: 23 },
          { id: 6, nombre: 'Libros', productos: 89 },
          { id: 7, nombre: 'Belleza', productos: 67 },
          { id: 8, nombre: 'Automóviles', productos: 12 },
        ];

        commit('SET_CATEGORIAS', categorias); // Actualizar el estado con las categorías
      }, 1000); // Simular un retardo de 1 segundo
    },
  },
  getters: {
    productosFiltrados: (state) => (categoria) => {
      if (!categoria) return state.productos;
      return state.productos.filter(p => 
        p.categoria.toLowerCase() === categoria.toLowerCase()
      );
    },
    categorias(state) {
      return state.categorias;
    },
  },
});
