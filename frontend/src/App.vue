<template>
   <div id="app">
    <!-- Header: Barra de navegación -->
    <header class="header">
      <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
          <!-- Logo -->
          <router-link to="/" class="navbar-brand">
            <img src="@/assets/Logo/logo.png" alt="PixelMarket Logo" class="logo">
          </router-link>

          <!-- Menú móvil -->
          <button 
            class="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
          >
            <span class="navbar-toggler-icon"></span>
          </button>

          <!-- Enlaces -->
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-center">
              <li class="nav-item mx-2">
                <router-link to="/categorias" class="nav-link">Categorías</router-link>
              </li>
              <li class="nav-item mx-2 position-relative">
                <router-link to="/checkout" class="nav-link">
                  <i class="fas fa-shopping-cart"></i>
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

    <!-- Barra de búsqueda solo en la página principal -->
    <SearchBar v-if="$route.name === 'Home'" />

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
// Importa el componente SearchBar
import SearchBar from './components/SearchBar.vue';

export default {
  name: 'App',
  components: { SearchBar } // Asegúrate de que SearchBar esté registrado aquí
};
</script>

<style>
/* Estilos globales minimalistas */

/* Estilos para el logo */
/* Variables CSS */
:root {
  --color-primary: #047ffa;
  --color-error: #e74c3c;
  --color-success: #2ecc71;
  --border-radius: 8px;
  --transition-speed: 0.3s;
  --color-text: #2d3436; /* Gris oscuro para texto */
  --color-background: #f8f9fa; /* Fondo claro */
  --color-white: #ffffff; /* Blanco */
}

/* Estilos globales */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text);
  background-color: var(--color-background);
}

/* Estilos para el logo */
.logo {
  height: 111px; 
  width: auto;
  transition: transform var(--transition-speed) ease;
  margin: -10px 0; /* Ajustamos el margen para compensar el tamaño */
}

.logo:hover {
  transform: scale(1.05); /* Efecto hover sutil */
}

/* Estilos para la barra de navegación */
.navbar {
  max-height: 60px; /* Limita la altura de la barra de navegación */
  overflow: hidden; /* Evita que el contenido desborde */
  padding: 0.5rem 0; /* Ajusta el padding para mantener la altura */
}

.navbar-brand {
  padding: 0; /* Elimina el padding del contenedor del logo */
}

/* Barra de búsqueda */
.search-bar {
  display: flex;
  align-items: center;
  padding: 1rem;
}

.search-bar input {
  width: calc(100% - 100px); /* Ajusta el ancho del input */
  padding: 12px;
  border-radius: var(--border-radius);
  border: 2px solid #ecf0f1;
}

.search-bar input:focus {
  border-color: var(--color-primary);
}

.search-bar button {
  padding: 12px;
  background-color: var(--color-primary);
  color: white;
  border-radius: var(--border-radius);
  cursor: pointer;
}

/* Encabezados */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-weight: 600; /* Semi-bold */
  color: var(--color-text);
  margin-bottom: calc(1rem * 0.5);
}

h1 { font-size: 2.5rem; } /* 40px */
h2 { font-size: 2rem; }   /* 32px */
h3 { font-size: 1.75rem; }/* 28px */
h4 { font-size: 1.5rem; } /* 24px */
h5 { font-size: 1.25rem; }/* 20px */
h6 { font-size: 1rem; }   /* 16px */

/* Párrafos */
p {
  margin-bottom: 1rem;
  color: var(--color-text);
}

/* Enlaces */
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-speed) ease;
}

a:hover {
  color: darken(var(--color-primary), 10%);
}

/* Botones */
button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  font-weight: 500;
  padding: calc(1rem * 0.5) calc(1rem * 1);
  border: none;
  border-radius: var(--border-radius);
  background-color: var(--color-primary);
  color: var(--color-white);
  cursor: pointer;
  transition: background-color var(--transition-speed) ease;
}

button:hover {
  background-color: darken(var(--color-primary), 10%);
}

/* Formularios */
input, textarea, select {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  padding: calc(1rem * 0.5);
  border: 1px solid #ecf0f1;
  border-radius: var(--border-radius);
  width: 100%;
  margin-bottom: 1rem;
}

/* Contenedores */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 calc(1rem * 1);
}

/* Utilidades */
.text-center { text-align: center; }
.text-primary { color: var(--color-primary); }
.text-secondary { color: #6c757d; }
.bg-white { background-color: var(--color-white); }
.shadow-sm { box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }

/* Footer estilos */
.footer {
   margin-top :20px
}
</style>