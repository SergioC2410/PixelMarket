from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario, Ubicacion, MetodoPago
from .serializers import (
    UsuarioBaseSerializer,
    UsuarioRegistroSerializer,
    UsuarioActualizacionSerializer,
    UsuarioDetalleSerializer,
    UbicacionSerializer,
    MetodoPagoSerializer
)
from .permissions import EsPropietario

# ----------------------------
# Vistas de Autenticación (Mejoradas)
# ----------------------------
@api_view(['POST'])
def registro_usuario(request):
    """Registro de usuario con manejo de errores detallado"""
    serializer = UsuarioRegistroSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        refresh = RefreshToken.for_user(usuario)
        return Response({
            'mensaje': 'Registro exitoso',
            'usuario': UsuarioBaseSerializer(usuario).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def iniciar_sesion(request):
    """Inicio de sesión con tokens JWT"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Se requieren email y contraseña'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    usuario = authenticate(request, email=email, password=password)
    if not usuario:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    login(request, usuario)
    refresh = RefreshToken.for_user(usuario)
    return Response({
        'mensaje': 'Inicio de sesión exitoso',
        'usuario': UsuarioBaseSerializer(usuario).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cerrar_sesion(request):
    """Cierre de sesión con JWT"""
    logout(request)
    return Response(
        {'mensaje': 'Sesión cerrada exitosamente'},
        status=status.HTTP_200_OK
    )

# ----------------------------
# Vistas de Perfil (Mejoradas)
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_perfil_completo(request):
    """Obtiene todos los datos del usuario incluyendo ubicación y métodos de pago"""
    usuario = request.user
    serializer = UsuarioDetalleSerializer(usuario)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_perfil(request):
    """Actualización parcial del perfil"""
    usuario = request.user
    serializer = UsuarioActualizacionSerializer(
        instance=usuario,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'mensaje': 'Perfil actualizado', 'usuario': serializer.data},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------
# Vistas de Ubicación
# ----------------------------
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

# ----------------------------
# Vista de Eliminación de Cuenta
# ----------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_cuenta(request):
    """Elimina la cuenta del usuario autenticado"""
    usuario = request.user
    usuario.delete()
    return Response(
        {'mensaje': 'Cuenta eliminada exitosamente'},
        status=status.HTTP_204_NO_CONTENT
    )