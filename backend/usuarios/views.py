from django.contrib.auth import authenticate, login, logout  # Para autenticar y manejar la sesión del usuario
from django.http import JsonResponse  # Para devolver respuestas en formato JSON
from django.shortcuts import get_object_or_404  # Para obtener un objeto o devolver un error 404 si no existe

# Importamos herramientas de Django REST Framework (DRF)
from rest_framework.decorators import api_view, permission_classes  # Para definir vistas de API y proteger rutas
from rest_framework.permissions import IsAuthenticated  # Para restringir el acceso a usuarios autenticados
from rest_framework.response import Response  # Para devolver respuestas en formato JSON
from .serializers import UsuarioBaseSerializer, UsuarioRegistroSerializer, UsuarioActualizacionSerializer   # Importamos el serializador para el modelo Usuario

# Importamos JWT (JSON Web Tokens) para la autenticación
from rest_framework_simplejwt.tokens import RefreshToken  # Para generar tokens JWT

# Importamos el modelo de usuario personalizado
from .models import Usuario  # Importamos el modelo Usuario definido en models.py

from .models import Usuario, Ubicacion, MetodoPago
from .serializers import (
    UsuarioBaseSerializer,
    UsuarioRegistroSerializer,
    UsuarioActualizacionSerializer,
    UbicacionSerializer,
    MetodoPagoSerializer
)
from .permissions import EsPropietario

@api_view(['POST'])
def registro_usuario(request):
    serializer = UsuarioRegistroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Usuario registrado exitosamente'}, status=201)
    return Response(serializer.errors, status=400)

# Vista para iniciar sesión
@api_view(['POST'])
def iniciar_sesion(request):
    """
    Vista para iniciar sesión.
    """
    try:
        data = request.data  # Obtenemos los datos de la solicitud
        email = data.get('email')  # Obtenemos el nombre de usuario
        password = data.get('password')  # Obtenemos la contraseña

        usuario = authenticate(request, email=email, password=password)  # Autenticamos al usuario
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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_perfil_completo(request):
    """
    Vista para obtener la información del usuario autenticado.
    """
    usuario = request.user  # Obtenemos el usuario autenticado
    serializer = UsuarioBaseSerializer(usuario)  # Usamos UsuarioBaseSerializer
    
    return Response(serializer.data, status=200)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_perfil(request):
    usuario = request.user  # Usuario autenticado
    serializer = UsuarioActualizacionSerializer(
        instance=usuario,
        data=request.data,
        partial=True  # Permite actualización parcial
    )
    
    if serializer.is_valid():
        serializer.save()  # Guarda solo los campos permitidos
        return Response({'mensaje': 'Datos actualizados correctamente'})
    
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])  # Solo permite solicitudes DELETE
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder a esta vista
def eliminar_cuenta(request, user_id):
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
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def gestionar_ubicacion(request):
    """Obtiene o actualiza la ubicación del usuario"""
    usuario = request.user
    ubicacion, created = Ubicacion.objects.get_or_create(usuario=usuario)
    
    if request.method == 'GET':
        serializer = UbicacionSerializer(ubicacion)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UbicacionSerializer(ubicacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------
# Vistas de Métodos de Pago
# ----------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_metodos_pago(request):
    """Lista o crea métodos de pago del usuario"""
    if request.method == 'GET':
        metodos = MetodoPago.objects.filter(usuario=request.user, activo=True)
        serializer = MetodoPagoSerializer(metodos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MetodoPagoSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, EsPropietario])
def detalle_metodo_pago(request, pk):
    """Gestiona un método de pago específico"""
    metodo = get_object_or_404(MetodoPago, pk=pk, usuario=request.user)
    
    if request.method == 'GET':
        serializer = MetodoPagoSerializer(metodo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MetodoPagoSerializer(
            metodo,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        metodo.delete()
        return Response(
            {'mensaje': 'Método de pago eliminado'},
            status=status.HTTP_204_NO_CONTENT
        )
