<template>
  <div class="search-bar" :class="{ focused: isFocused }">
    <input
      ref="searchInput"
      type="text"
      v-model="searchQuery"
      placeholder="Buscar productos..."
      @input="handleSearchInput"
      @keyup.enter="executeSearch"
      @focus="isFocused = true"
      @blur="isFocused = false"
      class="search-input"
      aria-label="Buscar productos"
    />
    <button 
      @click="executeSearch" 
      class="search-button"
      :disabled="isSearching"
      aria-label="Ejecutar búsqueda"
    >
      <span class="button-text">{{ isSearching ? 'Buscando...' : 'Buscar' }}</span>
      <span class="button-icon">
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
        </svg>
      </span>
    </button>
  </div>
</template>

<script>
import { debounce } from 'lodash';

export default {
  name: 'SearchBar',
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      searchQuery: this.value,
      isFocused: false,
      isSearching: false
    };
  },
  watch: {
    value(newVal) {
      this.searchQuery = newVal;
    }
  },
  methods: {
    // Debounce para búsquedas mientras se escribe
    handleSearchInput: debounce(function() {
      this.$emit('input', this.searchQuery);
      this.$emit('search', this.searchQuery);
    }, 300),

    // Ejecutar búsqueda completa
    async executeSearch() {
  if (!this.searchQuery.trim()) return;

  this.isSearching = true;
  try {
    this.$emit('search-submit', this.searchQuery);
    // Cambiar de 'query' a 'params'
    await this.$router.push({
      name: 'search',
      params: { query: this.searchQuery }  // Usar 'params' en vez de 'query'
    });
  } finally {
    this.isSearching = false;
  }
},


    // Enfocar el input programáticamente
    focus() {
      this.$refs.searchInput.focus();
    }
  }
};
</script>

<style scoped>
.search-bar {
  --primary-color: #3b82f6;
  --primary-light: #93c5fd;
  --transition-speed: 0.3s;
  
  display: flex;
  align-items: center;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  border-radius: 50px;
  transition: all var(--transition-speed) ease;
  background: white;
  border: 1px solid var(--primary-light);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transform: scale(1);
}

.search-bar.focused {
  transform: scale(0.98);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
  border-color: var(--primary-color);
}

.search-input {
  flex: 1;
  padding: 14px 24px;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: 1rem;
  outline: none;
  transition: all var(--transition-speed) ease;
  background: transparent;
  color: #333;
  height: 100%;
}

.search-input::placeholder {
  color: #9ca3af;
  transition: all var(--transition-speed) ease;
}

.search-bar.focused .search-input::placeholder {
  opacity: 0.5;
}

.search-button {
  padding: 0 20px;
  border: none;
  background: var(--primary-color);
  color: white;
  border-radius: 0 50px 50px 0;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--transition-speed) ease;
  height: 48px;
  min-width: 100px;
}

.search-button:hover:not(:disabled) {
  background: var(--primary-light);
}

.search-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.search-button:active:not(:disabled) {
  transform: scale(0.96);
}

.button-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-speed) ease;
}

.search-button:hover:not(:disabled) .button-icon {
  transform: rotate(10deg);
}

.button-text {
  transition: all var(--transition-speed) ease;
}

.search-button:hover:not(:disabled) .button-text {
  letter-spacing: 0.5px;
}

/* Efecto de onda al hacer clic */
.search-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 70%);
  transform: scale(0);
  opacity: 0;
  pointer-events: none;
}

.search-button:active:not(:disabled)::after {
  animation: ripple var(--transition-speed) linear;
}

@keyframes ripple {
  to {
    transform: scale(2);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .search-bar {
    max-width: 100%;
    border-radius: 30px;
  }
  
  .search-input {
    padding: 12px 16px;
    font-size: 0.9rem;
  }
  
  .search-button {
    padding: 0 16px;
    min-width: 80px;
    font-size: 0.9rem;
    height: 44px;
  }
  
  .button-text {
    display: none;
  }
  
  .search-button {
    width: 44px;
    min-width: 44px;
    justify-content: center;
  }
}
</style>