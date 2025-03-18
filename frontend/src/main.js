import { createApp } from 'vue';  // Importa la función createApp de Vue
import App from './App.vue';      // Importa el componente principal App.vue
import router from './router';    // Importa el router (que creamos en src/router/index.js)
import 'bootstrap/dist/css/bootstrap.css';  // Importa Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.js';    // Importa Bootstrap JS




// Importa los estilos de SweetAlert2
import 'sweetalert2/dist/sweetalert2.min.css';
// Crea la aplicación Vue
const app = createApp(App);

// Usa el router
app.use(router);

// Monta la aplicación en el elemento con id "app" en el archivo index.html
app.mount('#app');
