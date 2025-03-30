"""
Este módulo contiene las vistas para manejar pedidos en la aplicación.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from productos.models import Producto
from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer, ItemPedidoSerializer

# Constantes
PEDIDO_NO_ENCONTRADO = 'Pedido no encontrado'

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pedido(request):
    """
    Vista para crear un nuevo pedido.
    """
    if request.method == 'POST':
        try:
            data = request.data
            usuario_id = data.get('usuario_id')
            items = data.get('items', [])

            if not items:
                return Response({'error': 'El pedido no puede estar vacío'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear el pedido
            pedido = Pedido.objects.create(usuario_id=usuario_id)

            # Procesar cada ítem del pedido
            for item in items:
                producto_id = item.get('producto_id')
                cantidad = item.get('cantidad', 1)

                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    pedido.delete()  # Eliminar el pedido si el producto no existe
                    return Response({'error': f'Producto con ID {producto_id} no encontrado'}, status=status.HTTP_404_NOT_FOUND)

                if cantidad > producto.stock:
                    pedido.delete()  # Eliminar el pedido si no hay suficiente stock
                    return Response({'error': f'No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}'}, status=status.HTTP_400_BAD_REQUEST)

                # Crear el ítem de pedido
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

            # Calcular el total del pedido
            pedido.calcular_total()

            return Response({'mensaje': 'Pedido creado exitosamente', 'pedido_id': pedido.id}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_pedidos(request):
    """
    Vista para listar todos los pedidos de un usuario.
    """
    if request.method == 'GET':
        usuario_id = request.query_params.get('usuario_id')

        if not usuario_id:
            return Response({'error': 'Se requiere el ID del usuario'}, status=status.HTTP_400_BAD_REQUEST)

        pedidos = Pedido.objects.filter(usuario_id=usuario_id).select_related('usuario').prefetch_related('items')
        serializer = PedidoSerializer(pedidos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_pedido(request, pedido_id):
    """
    Vista para obtener los detalles de un pedido específico.
    """
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pedido.DoesNotExist:
        return Response({'error': PEDIDO_NO_ENCONTRADO}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_pedido(request, pedido_id):
    """
    Vista para actualizar un pedido (por ejemplo, cambiar el estado).
    """
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        serializer = PedidoSerializer(pedido, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Pedido.DoesNotExist:
        return Response({'error': PEDIDO_NO_ENCONTRADO}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancelar_pedido(request, pedido_id):
    """
    Vista para cancelar un pedido.
    """
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.estado = 'cancelado'  # Asegúrate de que el campo se llame 'estado' en tu modelo
        pedido.save()
        return Response({'mensaje': 'Pedido cancelado exitosamente'}, status=status.HTTP_200_OK)
    except Pedido.DoesNotExist:
        return Response({'error': PEDIDO_NO_ENCONTRADO}, status=status.HTTP_404_NOT_FOUND)