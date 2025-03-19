import axios from 'axios';

// Configura la URL base de tu API
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/', // Cambia esta URL a la de tu backend
  timeout: 10000, // Tiempo de espera máximo de 10 segundos
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
