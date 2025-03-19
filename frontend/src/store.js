import { createStore } from 'vuex'; // Usa 'createStore' en lugar de 'Vuex.Store'
import axios from 'axios';

export default createStore({
  state: {
    categorias: [],
    productos: [],
    cargando: false,
  },
  getters: {
    categorias: state => state.categorias,
    productosFiltrados: (state) => (categoria) => {
      return state.productos.filter(p => p.categoria === categoria);
    },
    cargando: state => state.cargando,
  },
  mutations: {
    setCategorias(state, categorias) {
      state.categorias = categorias;
    },
    setProductos(state, productos) {
      state.productos = productos;
    },
    setCargando(state, cargando) {
      state.cargando = cargando;
    },
  },
  actions: {
    async cargarCategorias({ commit }) {
      commit('setCargando', true);
      try {
        // Ejemplo de llamada a una API para obtener categorías
        const response = await axios.get('/api/categorias');
        commit('setCategorias', response.data);
      } catch (error) {
        console.error('Error al cargar categorías:', error);
      } finally {
        commit('setCargando', false);
      }
    },
    async cargarProductos({ commit }) {
      commit('setCargando', true);
      try {
        // Ejemplo de llamada a una API para obtener productos
        const response = await axios.get('/api/productos');
        commit('setProductos', response.data);
      } catch (error) {
        console.error('Error al cargar productos:', error);
      } finally {
        commit('setCargando', false);
      }
    },
  },
});
