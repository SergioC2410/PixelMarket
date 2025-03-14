<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link to="/" class="navbar-brand">PixelMarket</router-link>
        <div class="navbar-nav">
          <router-link to="/login" class="nav-link">Login</router-link>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'MiNavbar'  // Cambia "Navbar" a "MiNavbar"
  };
  </script>
  
  <style scoped>
  /* Estilos específicos para el Navbar */
  </style>