import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router';
import store from '@/store';
import { BootstrapVue3 } from 'bootstrap-vue-3';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import 'bootstrap/dist/js/bootstrap.js';
import Swal from 'sweetalert2';

// 🔥 Importa el componente de rating
import StarRating from 'vue-star-rating';

const app = createApp(App);

// Configuraciones principales
app.use(router);
app.use(store);
app.use(BootstrapVue3);
app.config.globalProperties.$swal = Swal;

// 🌟 Registra el componente globalmente (opcional)
app.component('StarRating', StarRating);

app.mount('#app');
