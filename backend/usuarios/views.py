# Este archivo contiene la lógica para manejar las solicitudes HTTP (APIs).
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
import json

@csrf_exempt
def registro_usuario(request):
    """
    Vista para registrar un nuevo usuario.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            rol = data.get('rol', 'comprador')  # Rol por defecto: comprador

            # Crear el usuario
            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                password=password,
                rol=rol
            )
            return JsonResponse({'mensaje': 'Usuario registrado exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def iniciar_sesion(request):
    """
    Vista para iniciar sesión.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Autenticar al usuario
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return JsonResponse({'mensaje': 'Inicio de sesión exitoso'}, status=200)
            else:
                return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def cerrar_sesion(request):
    """
    Vista para cerrar sesión.
    """
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'mensaje': 'Sesión cerrada exitosamente'}, status=200)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Mejoras sugeridas:
# 1. Agregar validaciones adicionales (ej: correo único).
# 2. Implementar JWT (JSON Web Tokens) para autenticación más segura.
# 3. Agregar pruebas unitarias para cada vista.