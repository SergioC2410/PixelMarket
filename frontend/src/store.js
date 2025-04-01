import { createStore } from 'vuex';
import axiosInstance from '@/util/axios';

const construirUrlCompleta = (imagenPath) => {
  if (!imagenPath) return null;
  if (imagenPath.startsWith('http')) return imagenPath;
  
  const baseUrl = process.env.NODE_ENV === 'production' 
    ? 'https://tudominio.com/media/' 
    : 'http://localhost:8000/media/';
  
  return baseUrl + imagenPath;
};

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
    productosConDescuento: [],
    cartItems: JSON.parse(localStorage.getItem('cart')) || [],
    exchangeRate: 36.5 // Tasa de cambio por defecto
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
    
    // Getters para el carrito
    cartItemCount: (state) => {
      return state.cartItems.reduce((count, item) => count + item.quantity, 0);
    },
    cartTotal: (state) => {
      return state.cartItems.reduce((total, item) => {
        return total + (item.price * item.quantity);
      }, 0);
    },
    cartTotalWithDiscount: (state) => {
      return state.cartItems.reduce((total, item) => {
        const discount = (item.price * item.quantity * (item.discountPercentage || 0)) / 100;
        return total + (item.price * item.quantity) - discount;
      }, 0);
    },
    cartTotalDiscount: (state) => {
      return state.cartItems.reduce((total, item) => {
        return total + ((item.price * item.quantity * (item.discountPercentage || 0)) / 100);
      }, 0);
    },
    
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
        itemsPerPage: 10 // Valor fijo para la paginación del cliente
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
    },

    // Mutaciones para el carrito
    ADD_TO_CART(state, { product, quantity }) {
      const existingItem = state.cartItems.find(item => item.id === product.id);
      
      if (existingItem) {
        existingItem.quantity += quantity;
      } else {
        state.cartItems.push({
          ...product,
          quantity,
          discountPercentage: product.descuento_aplicado || 0
        });
      }
      localStorage.setItem('cart', JSON.stringify(state.cartItems));
    },
    
    REMOVE_FROM_CART(state, productId) {
      state.cartItems = state.cartItems.filter(item => item.id !== productId);
      localStorage.setItem('cart', JSON.stringify(state.cartItems));
    },
    
    UPDATE_CART_ITEM_QUANTITY(state, { productId, quantity }) {
      const item = state.cartItems.find(item => item.id === productId);
      if (item) {
        item.quantity = quantity;
      }
      localStorage.setItem('cart', JSON.stringify(state.cartItems));
    },
    
    CLEAR_CART(state) {
      state.cartItems = [];
      localStorage.removeItem('cart');
    },

    SET_EXCHANGE_RATE(state, rate) {
      state.exchangeRate = rate;
    }
  },
  
  actions: {
    async login({ commit }, credenciales) {
      try {
        const { data } = await axiosInstance.post('auth/login/', credenciales);
        commit('SET_TOKEN', data.token);
        return true;
      } catch (error) {
        const errorMessage = error.response?.data?.message || 'Error de autenticación';
        commit('SET_ERROR', errorMessage);
        return false;
      }
    },

    logout({ commit }) {
      commit('CLEAR_TOKEN');
      commit('SET_PRODUCTO_ACTUAL', null);
    },

    async cargarCategorias({ commit, state }) {
      if (state.categorias.length > 0) return;

      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const { data } = await axiosInstance.get('categorias/');
        commit('SET_CATEGORIAS', data);
      } catch (error) {
        const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail || 
                          error.message || 
                          'Error al cargar categorías';
        commit('SET_ERROR', errorMessage);
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async cargarProductos({ commit, state }, params = {}) {
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        // Obtenemos todos los productos sin paginación del servidor
        const { data } = await axiosInstance.get('productos/', { 
          params: {
            ...params,
            page_size: 1000 // Número grande para obtener todos los productos
          } 
        });

        const productos = (data.results || []).map(producto => ({
          ...producto,
          imagen: construirUrlCompleta(producto.imagen),
          precio: Number(producto.precio)
        }));
        
        commit('SET_PRODUCTOS', productos);
        commit('SET_PAGINACION', {
          currentPage: 1,
          totalPages: Math.ceil(productos.length / state.paginacion.itemsPerPage),
          totalItems: productos.length
        });

        // Productos destacados
        const destacados = [...productos]
          .sort(() => 0.5 - Math.random())
          .slice(0, 4);
      
        // Productos con descuento
        const conDescuento = [...productos]
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
        
        commit('SET_PRODUCTOS_DESTACADOS', destacados);
        commit('SET_PRODUCTOS_CON_DESCUENTO', conDescuento);

        // Cachear todos los productos
        productos.forEach(producto => {
          commit('CACHE_PRODUCTO', producto);
        });

      } catch (error) {
        const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail || 
                          error.message || 
                          'Error al cargar productos';
        commit('SET_ERROR', errorMessage);
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async cargarProductoPorId({ commit, state }, productoId) {
      // Verificar caché primero
      if (state.productosCache[productoId]) {
        commit('SET_PRODUCTO_ACTUAL', state.productosCache[productoId]);
        return;
      }
    
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const { data } = await axiosInstance.get(`productos/${productoId}/`);
        
        // Procesar imágenes del producto
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
        const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail || 
                          error.message || 
                          'Error al cargar el producto';
        commit('SET_ERROR', errorMessage);
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async crearProducto({ commit }, productoData) {
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const formData = crearFormData(productoData);
        const { data } = await axiosInstance.post('productos/', formData);
        commit('AGREGAR_PRODUCTO', data);
        return data;
      } catch (error) {
        const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail || 
                          error.message || 
                          'Error al crear el producto';
        commit('SET_ERROR', errorMessage);
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async actualizarProducto({ commit }, { id, datos }) {
      commit('SET_CARGANDO', true);
      commit('SET_ERROR', null);
      
      try {
        const formData = crearFormData(datos);
        const { data } = await axiosInstance.patch(`productos/${id}/`, formData);
        commit('ACTUALIZAR_PRODUCTO', data);
        return data;
      } catch (error) {
        const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail || 
                          error.message || 
                          'Error al actualizar el producto';
        commit('SET_ERROR', errorMessage);
        throw error;
      } finally {
        commit('SET_CARGANDO', false);
      }
    },

    async agregarProductoAlCarrito({ commit, state }, { productoId, cantidad }) {
      try {
        // Buscar el producto en el cache o cargarlo si no está
        let producto = state.productosCache[productoId];
        
        if (!producto) {
          const { data } = await axiosInstance.get(`productos/${productoId}/`);
          producto = {
            id: data.id,
            name: data.nombre,
            price: data.precio,
            image: data.imagen ? construirUrlCompleta(data.imagen) : null,
            discountPercentage: data.descuento_aplicado || 0
          };
          commit('CACHE_PRODUCTO', producto);
        }
        
        commit('ADD_TO_CART', { product: producto, quantity: cantidad });
        return true;
      } catch (error) {
        const errorMessage = error.response?.data?.message || 
                          'Error al agregar producto al carrito';
        commit('SET_ERROR', errorMessage);
        throw error;
      }
    },

    async fetchExchangeRate({ commit }) {
      try {
        const apiKey = '486f0d2b81e7c30a7340fb24'; // Tu clave API de ExchangeRate-API
        const response = await axios.get(`https://v6.exchangerate-api.com/v6/${apiKey}/latest/USD`);
        commit('SET_EXCHANGE_RATE', response.data.conversion_rates.VES);
      } catch (error) {
        console.error('Error al obtener el tipo de cambio:', error);
        commit('SET_EXCHANGE_RATE', 36.5); // Valor por defecto en caso de error
      }
    }
  }
});