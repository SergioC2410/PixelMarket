<!-- SearchBar.vue -->
<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Buscar..."
      @input="handleSearch"
    />
    <button @click="handleSearchClick">Buscar</button>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    handleSearch() {
      console.log('Texto de búsqueda:', this.searchQuery);
    },
    handleSearchClick() {
      console.log('Buscar:', this.searchQuery);
      this.$router.push({ name: 'search', params: { query: this.searchQuery } });
    }
  }
};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  padding: 0.5rem; /* Aumenta el padding */
  width: 300px; /* Aumenta el ancho */
  margin: 0 auto; /* Centra la barra */
}

.search-bar input {
  padding: 0.2rem;
  border: none;
  border-radius: 4px 0 0 4px;
  width: 205px; /* Ajusta el ancho del input */
}

.search-bar button {
  padding: 0.2rem;
  border: none;
  background-color: #047ffa;
  color: white;
  border-radius:  8px 8px ;
  cursor: pointer;
  width: 80px; /* Ajusta el ancho del botón */
}

</style>
