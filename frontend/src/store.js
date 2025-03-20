import { createStore } from 'vuex';
import axiosInstance from '@/util/axios';

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
        const response = await axiosInstance.get('categorias/'); // Usa axiosInstance
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
        const response = await axiosInstance.get('productos/'); // Usa axiosInstance
        commit('setProductos', response.data);
      } catch (error) {
        console.error('Error al cargar productos:', error);
      } finally {
        commit('setCargando', false);
      }
    },
  },
});
