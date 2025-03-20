import { createApp } from 'vue';  // Importa la función createApp de Vue
import App from '@/App.vue';      // Importa el componente principal App.vue
import router from '@/router';    // Importa el router (que creamos en src/router/index.js)
import 'bootstrap/dist/css/bootstrap.css';  // Importa Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.js';    // Importa Bootstrap JS
import store from './store'; // Importa el store que acabamos de configurar


// Crea la aplicación Vue
const app = createApp(App);

// Usa el router y el store
app.use(router);  // Configura Vue Router para navegación
app.use(store);   // Configura Vuex para gestionar el estado

// Monta la aplicación en el elemento con id "app" en el archivo index.html
app.mount('#app');

createApp(App).use(router).mount('#app');