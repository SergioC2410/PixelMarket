import { createStore } from 'vuex';
import axiosInstance from '@/util/axios';

export default createStore({
  state: {
    categorias: [],
    productos: [],
    cargando: false,
  },
  getters: {
    categorias: (state) => state.categorias,
    productosFiltrados: (state) => (categoria) =>
      state.productos.filter((p) => p.categoria === categoria),
    cargando: (state) => state.cargando,
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
        const response = await axiosInstance.get('categorias/');
        // Comprobamos que la respuesta es un array
        if (Array.isArray(response.data)) {
          commit('setCategorias', response.data);
        } else {
          console.error('La respuesta de categorías no es un array:', response.data);
          commit('setCategorias', []); // Asignamos un array vacío en caso de error
        }
      } catch (error) {
        console.error('Error al cargar categorías:', error);
        commit('setCategorias', []); // Asignamos un array vacío en caso de error
      } finally {
        commit('setCargando', false);
      }
    },
    async cargarProductos({ commit }) {
      commit('setCargando', true);
      try {
      const response = await axiosInstance.get('productos/');
      console.log('Respuesta de productos:', response.data);

      // Comprobamos si la respuesta tiene la estructura correcta
      if (response.data && Array.isArray(response.data.productos)) {
        commit('setProductos', response.data.productos); // Accedemos a la propiedad 'productos' de la respuesta
      } else {
        console.error('La respuesta de productos no tiene la estructura esperada:', response.data);
        commit('setProductos', []); // Asignamos un array vacío si no tiene la estructura esperada
      }
      } catch (error) {
      console.error('Error al cargar productos:', error);
      commit('setProductos', []); // Asignamos un array vacío en caso de error
      } finally {
      commit('setCargando', false);
      }
    },
  },
});
