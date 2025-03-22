import { createApp } from 'vue';                 // Importa la función createApp de Vue
import App from '@/App.vue';                     // Importa el componente principal App.vue
import router from '@/router';                   // Importa el router
import store from '@/store';                     // Importa el store de Vuex
import { BootstrapVue3 } from 'bootstrap-vue-3'; // Importa BootstrapVue3 para Vue 3
import 'bootstrap/dist/css/bootstrap.min.css';  // Estilos básicos de Bootstrap
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'; // Estilos de BootstrapVue3
import 'bootstrap/dist/js/bootstrap.js';        // Importa Bootstrap JS
import Swal from 'sweetalert2';                  // Importa SweetAlert2

// Crea la aplicación Vue
const app = createApp(App);

// Configura Vue Router, Vuex y BootstrapVue3
app.use(router);         // Navegación con Vue Router
app.use(store);          // Gestión del estado global con Vuex
app.use(BootstrapVue3);  // Componentes de BootstrapVue3
app.config.globalProperties.$swal = Swal; // Configura SweetAlert2 como propiedad global
// Monta la aplicación en el elemento con id "app" del archivo index.html
app.mount('#app');

