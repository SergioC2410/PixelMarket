<template>
  <div id="app">
    <header class="header">
      <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
          <!-- Logo a la izquierda - ahora más grande -->
          <router-link to="/" class="navbar-brand logo-wrapper me-lg-4">
            <img src="@/assets/Logo/logo.png" alt="PixelMarket Logo" class="logo-large">
          </router-link>

          <!-- Barra de búsqueda centrada -->
          <div class="search-bar-container mx-lg-4">
            <SearchBar v-if="$route.name === 'Home'" class="centered-search-bar" />
          </div>

          <!-- Menú hamburguesa -->
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>

          <!-- Menú de navegación a la derecha -->
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-center">
              <li class="nav-item mx-2">
                <router-link to="/productos" class="nav-link">Categorías</router-link>
              </li>
              <li class="nav-item mx-2 position-relative">
                <router-link to="/checkout" class="nav-link">
                  <i class="fas fa-shopping-cart fa-lg"></i>
                  <span class="badge bg-danger position-absolute top-0 start-100 translate-middle">0</span>
                </router-link>
              </li>
              <li class="nav-item mx-2">
                <router-link to="/login" class="btn btn-outline-primary">Ingresar</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <footer class="footer bg-white border-top py-4">
      <div class="container text-center">
        <p class="text-muted mb-0">&copy; 2025 PixelMarket - Todos los derechos reservados</p>
      </div>
    </footer>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue';

export default {
  name: 'App',
  components: { SearchBar }
};
</script>

<style>
:root {
  --color-primary: #047ffa;
  --color-primary-light: #4da8ff;
  --color-error: #e74c3c;
  --color-success: #2ecc71;
  --border-radius: 8px;
  --transition-speed: 0.3s;
}

/* Logo grande - ahora más grande y legible */
.logo-wrapper {
  padding: 0;
  display: flex;
  align-items: center;
  height: 100%;
}

.logo-large {
  height: 90px; /* Aumentado de 80px a 90px */
  width: auto;
  max-width: 350px; /* Aumentado de 300px a 350px */
  object-fit: contain;
  transition: all var(--transition-speed) ease;
  object-position: left center; /* Asegura que el texto del logo esté bien alineado */
}

/* Contenedor de barra de búsqueda */
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

/* Ajustes de navegación */
.navbar {
  padding: 0.5rem 0;
}

.nav-link {
  padding: 0.5rem 1rem;
  font-weight: 500;
}

/* Alineación de elementos en desktop */
@media (min-width: 992px) {
  .navbar-collapse {
    flex-basis: auto !important;
    flex-grow: 0 !important;
  }
  
  .navbar-brand {
    margin-right: 1rem !important;
  }
}

/* Responsive */
@media (max-width: 991.98px) {
  .logo-large {
    height: 80px; /* Aumentado de 70px a 80px */
    max-width: 300px; /* Aumentado de 250px a 300px */
  }
  
  .search-bar-container {
    order: 3;
    width: 100%;
    margin-top: 1rem;
    padding: 0;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  
  .navbar-collapse {
    margin-top: 1rem;
  }
}

@media (max-width: 767.98px) {
  .logo-large {
    height: 70px; /* Aumentado de 60px a 70px */
    max-width: 250px; /* Aumentado de 200px a 250px */
  }
}

.main-content {
  padding: 2rem 0;
  min-height: calc(100vh - 180px);
}
</style>