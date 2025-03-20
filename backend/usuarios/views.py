from django.contrib.auth import authenticate, login, logout  # Para autenticar y manejar la sesión del usuario
from django.http import JsonResponse  # Para devolver respuestas en formato JSON
from django.shortcuts import get_object_or_404  # Para obtener un objeto o devolver un error 404 si no existe

# Importamos herramientas de Django REST Framework (DRF)
from rest_framework.decorators import api_view, permission_classes  # Para definir vistas de API y proteger rutas
from rest_framework.permissions import IsAuthenticated  # Para restringir el acceso a usuarios autenticados
from rest_framework.response import Response  # Para devolver respuestas en formato JSON
from .serializers import UsuarioSerializer  # Importamos el serializador para el modelo Usuario

# Importamos JWT (JSON Web Tokens) para la autenticación
from rest_framework_simplejwt.tokens import RefreshToken  # Para generar tokens JWT

# Importamos el modelo de usuario personalizado
from .models import Usuario  # Importamos el modelo Usuario definido en models.py

@api_view(['POST'])
def registro_usuario(request):
    """
    Vista para registrar un nuevo usuario.
    """
    serializer = UsuarioSerializer(data=request.data)  # Creamos una instancia del serializador con los datos de la solicitud
    if serializer.is_valid():  # Verificamos si los datos son válidos
        serializer.save()  # Guardamos el nuevo usuario en la base de datos
        return Response({'mensaje': 'Usuario registrado exitosamente'}, status=201)  # Devolvemos una respuesta de éxito
    return Response(serializer.errors, status=400)  # Devolvemos los errores de validación

# Vista para iniciar sesión
@api_view(['POST'])
def iniciar_sesion(request):
    """
    Vista para iniciar sesión.
    """
    try:
        data = request.data  # Obtenemos los datos de la solicitud
        username = data.get('username')  # Obtenemos el nombre de usuario
        password = data.get('password')  # Obtenemos la contraseña

        usuario = authenticate(request, username=username, password=password)  # Autenticamos al usuario
        if usuario is not None:  # Si la autenticación es exitosa
            login(request, usuario)  # Iniciamos la sesión del usuario
            refresh = RefreshToken.for_user(usuario)  # Generamos un token de actualización (refresh token)
            return Response({
                'mensaje': 'Inicio de sesión exitoso',
                'refresh': str(refresh),  # Token de actualización
                'access': str(refresh.access_token),  # Token de acceso
            }, status=200)  # Devolvemos una respuesta de éxito con los tokens
        else:
            return Response({'error': 'Credenciales inválidas'}, status=401)  # Devolvemos un error si las credenciales son inválidas
    except Exception as e:
        return Response({'error': str(e)}, status=400)  # Devolvemos un error genérico si ocurre una excepción
    

# Vista para cerrar sesión
@api_view(['POST'])  # Solo permite solicitudes POST
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder a esta vista
def cerrar_sesion(request):
    """
    Vista para cerrar sesión. Solo usuarios autenticados pueden cerrar sesión.
    """
    logout(request)  # Cerramos la sesión del usuario
    return JsonResponse({'mensaje': 'Sesión cerrada exitosamente'}, status=200)  # Devolvemos una respuesta de éxito


# Vista para obtener la información del usuario autenticado
@api_view(['GET'])  # Solo permite solicitudes GET
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder a esta vista
def obtener_info_usuario(request):
    """
    Vista para obtener la información del usuario autenticado.
    """
    usuario = request.user  # Obtenemos el usuario autenticado
    serializer = UsuarioSerializer(usuario)  # Serializamos la información del usuario
    
    return Response(serializer.data, status=200)  # Devolvemos la información del usuario en la respuesta


@api_view(['PUT'])  # Solo permite solicitudes PUT
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder a esta vista
def actualizar_usuario(request, user_id):
    """
    Vista para actualizar completamente la información de un usuario.
    """
    usuario = get_object_or_404(Usuario, id=user_id)  # Obtenemos el usuario o devolvemos un error 404 si no existe
    if request.user != usuario:  # Verificamos que el usuario autenticado sea el mismo que se desea actualizar
        return Response({'error': 'No tienes permiso para actualizar este usuario'}, status=403)  # Devolvemos un error si no tiene permiso

    serializer = UsuarioSerializer(usuario, data=request.data)  # Creamos una instancia del serializador con los datos de la solicitud
    if serializer.is_valid():  # Verificamos si los datos son válidos
        serializer.save()  # Guardamos los cambios en la base de datos
        return Response({'mensaje': 'Usuario actualizado exitosamente'}, status=200)  # Devolvemos una respuesta de éxito
    return Response(serializer.errors, status=400)  # Devolvemos los errores de validación


@api_view(['PATCH'])  # Solo permite solicitudes PATCH
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder a esta vista
def actualizar_usuario_parcial(request, user_id):
    """
    Vista para actualizar parcialmente la información de un usuario.
    """
    usuario = get_object_or_404(Usuario, id=user_id)  # Obtenemos el usuario o devolvemos un error 404 si no existe
    if request.user != usuario:  # Verificamos que el usuario autenticado sea el mismo que se desea actualizar
        return Response({'error': 'No tienes permiso para actualizar este usuario'}, status=403)  # Devolvemos un error si no tiene permiso

    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)  # Creamos una instancia del serializador con los datos de la solicitud, permitiendo actualizaciones parciales
    if serializer.is_valid():  # Verificamos si los datos son válidos
        serializer.save()  # Guardamos los cambios en la base de datos
        return Response({'mensaje': 'Usuario actualizado exitosamente'}, status=200)  # Devolvemos una respuesta de éxito
    return Response(serializer.errors, status=400)  # Devolvemos los errores de validación


@api_view(['DELETE'])  # Solo permite solicitudes DELETE
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder a esta vista
def eliminar_usuario(request, user_id):
    """
    Vista para eliminar un usuario.
    Solo usuarios autenticados pueden eliminar su propia cuenta.
    """
    try:
        usuario = get_object_or_404(Usuario, id=user_id)  # Obtenemos el usuario que se desea eliminar

        if request.user != usuario:  # Verificamos que el usuario autenticado sea el mismo que se desea eliminar
            return JsonResponse({'error': 'No tienes permiso para eliminar este usuario'}, status=403)  # Devolvemos un error si no tiene permiso

        usuario.delete()  # Eliminamos el usuario de la base de datos

        return JsonResponse({'mensaje': 'Usuario eliminado exitosamente'}, status=200)  # Devolvemos una respuesta de éxito

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)  # Devolvemos un error genérico si ocurre una excepción