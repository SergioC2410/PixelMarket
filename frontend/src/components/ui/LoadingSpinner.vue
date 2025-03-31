<template>
    <div class="loading-spinner text-center py-5">
      <output class="spinner-border text-primary">
        <span class="visually-hidden">Cargando...</span>
      </output>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoadingSpinner'
  };
  </script>
  
  <style lang="scss" scoped>
  @import '@/assets/styles/variables.scss';
  
  .loading-spinner {
    .spinner-border {
      width: 3rem;
      height: 3rem;
    }
  }
  </style>