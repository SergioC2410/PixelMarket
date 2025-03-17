<template>
  <div id="app">
    <!-- Navbar estilo Mercado Libre -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
      <div class="container">
        <!-- Logo y enlace a la página principal -->
        <router-link to="/" class="navbar-brand">
          <span class="text-primary fw-bold">Pixel</span>
          <span class="text-success fw-bold">Market</span>
        </router-link>

        <!-- Botón para menú móvil -->
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Enlaces de navegación -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <!-- Enlace al catálogo (Sergio) -->
            <li class="nav-item">
              <router-link to="/productos" class="nav-link">Productos</router-link>
            </li>
            
            <!-- Enlace al carrito (Jekson) -->
            <li class="nav-item">
              <router-link to="/checkout" class="nav-link">Carrito</router-link>
            </li>
            
            <!-- Enlace al login (Mauro) -->
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Ingresar</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Contenido principal (se renderizarán las vistas del router) -->
    <main class="container mt-4">
      <router-view></router-view>
    </main>

    <!-- Footer estilo minimalista -->
    <footer class="bg-light py-4 mt-5">
      <div class="container text-center">
        <p class="text-muted mb-0">&copy; 2025 PixelMarket - Todos los derechos reservados</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
/* Estilos globales inspirados en Mercado Libre */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

.navbar-brand {
  font-size: 1.5rem;
  letter-spacing: -0.5px;
}

.nav-link {
  font-weight: 500;
  color: #333 !important;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #2962ff !important;
}

footer {
  margin-top: auto;
}
</style>