<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Buscar productos..."
      @input="handleSearch"
      @keyup.enter="handleSearchClick"
      class="search-input"
    />
    <button @click="handleSearchClick" class="search-button">
      <span class="button-text">Buscar</span>
      <span class="button-icon">
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
        </svg>
      </span>
    </button>
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
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  transition: all 0.3s ease;
  background: white;
  border: 1px solid var(--color-primary-light);
}

.search-bar:focus-within {
  box-shadow: 0 4px 25px rgba(4, 127, 250, 0.2);
  transform: translateY(-2px);
  border-color: var(--color-primary);
}

.search-input {
  flex: 1;
  padding: 15px 25px;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  background: transparent;
  color: #333;
}

.search-input::placeholder {
  color: #aaa;
  font-style: italic;
}

.search-input:focus {
  padding-left: 30px;
  color: var(--color-primary);
}

.search-button {
  padding: 15px 25px;
  border: none;
  background: var(--color-primary);
  color: white;
  border-radius: 0 50px 50px 0;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.search-button:hover {
  background: var(--color-primary-light);
  transform: translateX(2px);
}

.search-button:active {
  transform: scale(0.98);
}

.button-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.search-button:hover .button-icon {
  transform: rotate(10deg) scale(1.1);
}

.button-text {
  transition: all 0.3s ease;
}

.search-button:hover .button-text {
  letter-spacing: 0.5px;
}

.search-button::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
  transform: scale(0);
  opacity: 0;
  transition: transform 0.5s ease, opacity 1s ease;
}

.search-button:active::after {
  transform: scale(2);
  opacity: 1;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

@keyframes inputFocus {
  0% { box-shadow: inset 0 0 0 0 var(rgba(255, 255, 255, 0.979)); }
  100% { box-shadow: inset 0 0 0 2px var(rgba(255, 255, 255, 0.979)); }
}

.search-input:focus {
  animation: inputFocus 0.5s ease forwards;
}

@media (max-width: 768px) {
  .search-bar {
    max-width: 100%;
    border-radius: 30px;
  }
  
  .search-input {
    padding: 12px 20px;
  }
  
  .search-button {
    padding: 12px 20px;
  }
}
</style>