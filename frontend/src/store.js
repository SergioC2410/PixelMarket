import { createStore } from 'vuex';
import axiosInstance from '@/util/axios';

// Función para construir URLs completas de imágenes
const construirUrlCompleta = (imagenPath) => {
  if (!imagenPath) return null;
  if (imagenPath.startsWith('http')) return imagenPath;
  
  const baseUrl = process.env.NODE_ENV === 'production' 
    ? 'https://tudominio.com/media/' 
    : 'http://localhost:8000/media/';
  
  return baseUrl + imagenPath;
};

// Helper para crear FormData desde objetos
const crearFormData = (datos) => {
  const formData = new FormData();
  Object.entries(datos).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (value instanceof File) {
        formData.append(key, value, value.name);
      } else if (Array.isArray(value)) {
        value.forEach((item, index) => {
          formData.append(`${key}[${index}]`, item);
        });
      } else {
        formData.append(key, value);
      }
    }
  });
  return formData;
};

// Funciones helper
const _handleError = (error, dispatch) => {
  if (error.response) {
    const { status, data } = error.response;
    
    if (status === 401) {
      dispatch('logout');
      return 'Sesión expirada. Por favor ingrese nuevamente.';
    }
    
    return data.message || data.detail || `Error ${status}: ${data}`;
  }
  return error.message || 'Error de conexión';
};

const _seleccionarDestacados = (productos) => {
  return [...productos]
    .sort(() => 0.5 - Math.random())
    .slice(0, 4);
};

const _aplicarDescuentosAleatorios = (productos) => {
  return [...productos]
    .sort(() => 0.5 - Math.random())
    .slice(0, 4)
    .map(producto => {
      const descuento = Math.floor(Math.random() * 21) + 10; // 10-30%
      return {
        ...producto,
        descuento_aplicado: descuento,
        precio_original: producto.precio,
        precio_con_descuento: Number((producto.precio * (1 - descuento / 100)).toFixed(2))
      };
    });
};

export default createStore({
  state: {
    token: localStorage.getItem('token') || null,
    categorias: [],
    productos: [],
    productoActual: null,
    productosCache: {},
    cargando: false,
    error: null,
    paginacion: {
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: 10
    },
    productosDestacados: [],
    productosConDescuento: []
  },
  
  getters: {
    todasCategorias: (state) => state.categorias,
    todosProductos: (state) => state.productos,
    productoDetalle: (state) => state.productoActual,
    estaCargando: (state) => state.cargando,
    ultimoError: (state) => state.error,
    datosPaginacion: (state) => state.paginacion,
    estaAutenticado: (state) => !!state.token,
    productosDestacados: (state) => state.productosDestacados,
    productosConDescuento: (state) => state.productosConDescuento,

    productosPorCategoria: (state) => (categoriaId) => {
      return state.productos.filter(p => p.categoria?.id === categoriaId);
    },

    productosDisponibles: (state) => {
      return state.productos.filter(p => p.stock > 0);
    }
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },

    CLEAR_TOKEN(state) {
      state.token = null;
      localStorage.removeItem('token');
    },

    SET_CATEGORIAS(state, categorias) {
      state.categorias = categorias;
    },

    SET_PRODUCTOS(state, productos) {
      state.productos = productos;
    },

    SET_PRODUCTO_ACTUAL(state, producto) {
      state.productoActual = producto;
    },

    SET_CARGANDO(state, estado) {
      state.cargando = estado;
    },

    SET_ERROR(state, error) {
      state.error = error;
    },

    AGREGAR_PRODUCTO(state, producto) {
      state.productos.unshift(producto);
      state.productosCache[producto.id] = producto;
    },

    ACTUALIZAR_PRODUCTO(state, productoActualizado) {
      const index = state.productos.findIndex(p => p.id === productoActualizado.id);
      if (index !== -1) {
        state.productos.splice(index, 1, productoActualizado);
      }
      state.productosCache[productoActualizado.id] = productoActualizado;
    },

    SET_PAGINACION(state, { currentPage, totalPages, totalItems }) {
      state.paginacion = {
        currentPage: currentPage || 1,
        totalPages: totalPages || 1,
        totalItems: totalItems || 0,
        itemsPerPage: state.paginacion.itemsPerPage
      };
    },

    CACHE_PRODUCTO(state, producto) {
      state.productosCache[producto.id] = producto;
    },

    SET_PRODUCTOS_DESTACADOS(state, productos) {
      state.productosDestacados = productos;
    },

    SET_PRODUCTOS_CON_DESCUENTO(state, productos) {
      state.productosConDescuento = productos;
    }
  },
  
  actions: {
    async login({ commit }, credenciales) {
      try {
        const { data } = await axiosInstance.post('auth/login/', credenciales);
        commit('SET_TOKEN', data.token);
        return true;
      } catch (error) {
        commit('SET_ERROR', _handleError(error, this.dispatch));
        return false;
      }
    },

    logout({ commit }) {
      commit('CLEAR_TOKEN');
      commit('SET_PRODUCTO_ACTUAL', null);
    },

    async cargarCategorias({ commit, state, dispatch }) {
      if (state.categorias.length > 0) return;

      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const { data } = await axiosInstance.get('categorias/');
        commit('SET_CATEGORIAS', data);
      } catch (error) {
        commit('SET_ERROR', _handleError(error, dispatch));
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async cargarProductos({ commit, state, dispatch }, params = {}) {
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const { data } = await axiosInstance.get('productos/', { 
          params: {
            page: params.page || 1,
            page_size: params.itemsPerPage || state.paginacion.itemsPerPage,
            ...params
          } 
        });

        const productos = data.results || [];
        commit('SET_PRODUCTOS', productos);
        commit('SET_PAGINACION', {
          currentPage: data.current_page || 1,
          totalPages: data.total_pages || 1,
          totalItems: data.total_items || data.count || 0
        });

        const destacados = _seleccionarDestacados(productos);
        const conDescuento = _aplicarDescuentosAleatorios(productos);
        
        commit('SET_PRODUCTOS_DESTACADOS', destacados);
        commit('SET_PRODUCTOS_CON_DESCUENTO', conDescuento);

        productos.forEach(producto => {
          commit('CACHE_PRODUCTO', producto);
        });
      } catch (error) {
        commit('SET_ERROR', _handleError(error, dispatch));
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async cargarProductoPorId({ commit, state, dispatch }, productoId) {
      if (state.productosCache[productoId]) {
        commit('SET_PRODUCTO_ACTUAL', state.productosCache[productoId]);
        return;
      }
    
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const { data } = await axiosInstance.get(`productos/${productoId}/`);
        
        const productoConImagenes = {
          ...data,
          imagen_url: data.imagen ? construirUrlCompleta(data.imagen) : null,
          imagenes_adicionales: data.imagenes_adicionales?.map(img => ({
            ...img,
            url: construirUrlCompleta(img.url || img.imagen)
          })) || []
        };
        
        commit('SET_PRODUCTO_ACTUAL', productoConImagenes);
        commit('CACHE_PRODUCTO', productoConImagenes);
      } catch (error) {
        commit('SET_ERROR', _handleError(error, dispatch));
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async crearProducto({ commit, dispatch }, productoData) {
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const formData = crearFormData(productoData);
        const { data } = await axiosInstance.post('productos/', formData);
        commit('AGREGAR_PRODUCTO', data);
        return data;
      } catch (error) {
        commit('SET_ERROR', _handleError(error, dispatch));
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async actualizarProducto({ commit, dispatch }, { id, datos }) {
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const formData = crearFormData(datos);
        const { data } = await axiosInstance.patch(`productos/${id}/`, formData);
        commit('ACTUALIZAR_PRODUCTO', data);
        return data;
      } catch (error) {
        commit('SET_ERROR', _handleError(error, dispatch));
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    }
  }
});