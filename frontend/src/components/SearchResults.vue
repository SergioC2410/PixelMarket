<template>
    <div class="search-results">
      <h2>Resultados de búsqueda para "{{ query }}"</h2>
      <!-- Aquí puedes mostrar los resultados de búsqueda -->
      <ul>
        <li v-for="result in results" :key="result.id">{{ result.name }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SearchResults',
    props: {
      query: String
    },
    data() {
      return {
        results: [] // Simula resultados de búsqueda
      };
    },
    mounted() {
      // Simula búsqueda de resultados
      this.results = [
        { id: 1, name: 'Resultado 1' },
        { id: 2, name: 'Resultado 2' }
      ];
    }
  };
  </script>
  
  <style scoped>
  .search-results {
    padding: 2rem;
  }
  </style>
  