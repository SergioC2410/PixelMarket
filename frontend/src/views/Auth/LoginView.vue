<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    <form id="login-form">
        <label for="email">Correo electrónico:</label>
        <input type="email" id="email" required>

        <label for="password">Contraseña:</label>
        <input type="password" id="password" required>

        <button type="submit">Iniciar Sesión</button>
    </form>
    
    <p>¿No tienes cuenta? >Regístrate<</p>
</div>
  </template>
  
  <script>
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    // Simulación de autenticación (reemplaza con tu lógica de autenticación real)
    if (email === 'mauro@123.com' && password === '123') {
        // Redirige a la página principal
        window.location.replace('INDEX.HTML');
    } else {
        alert('Correo electrónico o contraseña incorrectos');
    }
});

  </script>
  
  <style scoped>
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 0;
}

.login-container {
    width: 300px;
    padding: 20px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

.login-container h2 {
    margin-top: 0;
    color: #007bff;
}

#login-form {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
}

#login-form label {
    margin-bottom: 5px;
    font-weight: bold;
}

#login-form input {
    padding: 10px;
    margin-bottom: 15px;
    border: 3px solid #616a6b; 
    border-radius: 5px;
    transition: border-color 0.3s ease;
}

#login-form input:focus {
    border-color: #007bff; 
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); 
}

#login-form button {
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    font-weight: bold;
}

#login-form button:hover {
    background-color: #0056b3;
}

.login-container p {
    margin-top: 10px;
}

.login-container a {
    text-decoration: none;
    color: #007bff;
}

.login-container a:hover {
    text-decoration: underline;
}

  </style>