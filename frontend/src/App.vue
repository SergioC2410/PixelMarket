<template>
  <div id="app">
    <!-- Header con navegación y barra de búsqueda siempre visible -->
    <header class="header">
      <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
          <!-- Logo a la izquierda con animación al pasar el mouse -->
          <router-link to="/" class="navbar-brand logo-wrapper me-lg-4">
            <img src="@/assets/Logo/logo.png" alt="PixelMarket Logo" class="logo-large">
          </router-link>

          <!-- Barra de búsqueda centrada - siempre visible -->
          <div class="search-bar-container mx-lg-4">
            <SearchBar class="centered-search-bar" />
          </div>

          <!-- Menú hamburguesa para dispositivos móviles -->
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>

          <!-- Menú de navegación a la derecha -->
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-center">
              <li class="nav-item mx-2">
                <router-link to="/productos" class="nav-link">Productos</router-link>
              </li>
              <li class="nav-item mx-2 position-relative">
                <CartDropdown />
              </li>
              <li class="nav-item mx-2">
                <router-link to="/login" class="btn btn-outline-primary">Ingresar</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <!-- Contenido principal -->
    <main class="main-content">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="footer bg-white border-top py-4">
      <div class="container text-center">
        <p class="text-muted mb-0">&copy; 2025 PixelMarket - Todos los derechos reservados</p>
      </div>
    </footer>
  </div>
</template>

<script>
// Importamos el componente SearchBar para mostrarlo siempre
import SearchBar from './components/SearchBar.vue';
import CartDropdown from './components/CartDropdown.vue';

export default {
  name: 'App',
  components: { SearchBar, CartDropdown }
};
</script>

<style>
/* Variables de color y estilo global */
:root {
  --color-primary: #047ffa;
  --color-primary-light: #4da8ff;
  --color-error: #e74c3c;
  --color-success: #2ecc71;
  --border-radius: 8px;
  --transition-speed: 0.3s;
}

/* Logo más pequeño y con animación */
.logo-wrapper {
  padding: 0;
  display: flex;
  align-items: center;
  height: 100%;
  transition: transform var(--transition-speed) ease-in-out;
}

.logo-wrapper:hover .logo-large {
  transform: scale(1.1); /* Aumenta el logo al pasar el mouse */
}

/* Logo con animación */
.logo-large {
  height: 100px; /* Reducción de tamaño */
  width: auto;
  max-width: 300px; /* Tamaño del logo ajustado */
  object-fit: contain;
  transition: all var(--transition-speed) ease-in-out;
  object-position: left center;
}

/* Contenedor de la barra de búsqueda */
.search-bar-container {
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 0 1rem;
  min-width: 200px;
}

.centered-search-bar {
  width: 100%;
  max-width: 500px;
}

/* Estilo del menú de navegación */
.navbar {
  padding: 0.5rem 0;
}

.nav-link {
  padding: 0.5rem 1rem;
  font-weight: 500;
  transition: color var(--transition-speed) ease-in-out;
}

/* Animación llamativa en el menú de navegación */
.nav-link:hover {
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary), 0 0 20px var(--color-primary); /* Sombra de texto para efecto llamativo */
  transform: scale(1.1); /* Efecto de aumento al pasar el mouse */
}

/* Ajustes de navegación en dispositivos grandes */
@media (min-width: 992px) {
  .navbar-collapse {
    flex-basis: auto !important;
    flex-grow: 0 !important;
  }

  .navbar-brand {
    margin-right: 1rem !important;
  }
}

/* Responsive: ajustes para pantallas medianas */
@media (max-width: 991.98px) {
  .logo-large {
    height: 80px; /* Logo más pequeño en pantallas medianas */
    max-width: 250px;
  }

  .search-bar-container {
    order: 3;
    width: 100%;
    margin-top: 1rem;
    padding: 0;
  }

  .navbar-collapse {
    margin-top: 1rem;
  }
}

/* Ajustes para pantallas aún más pequeñas */
@media (max-width: 767.98px) {
  .logo-large {
    height: 70px; /* Logo aún más pequeño en pantallas pequeñas */
    max-width: 230px;
  }
}

/* Estilo para el contenido principal */
.main-content {
  padding: 2rem 0;
  min-height: calc(100vh - 180px);
}

/* Estilos para el dropdown del carrito */
.cart-dropdown {
  position: relative;
  display: inline-block;
}

.cart-toggle {
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
}

.cart-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  font-size: 0.7rem;
  background-color: var(--color-error);
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>