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

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Proteger la vista con autenticación
def crear_pedido(request):
    """
    Vista para crear un nuevo pedido.
    """
    if request.method == 'POST':
        try:
            # Obtener los datos del request. DRF ya maneja el JSON automáticamente.
            data = request.data

            # Obtener el ID del usuario y la lista de ítems del pedido.
            usuario_id = data.get('usuario_id')
            items = data.get('items', [])  # Lista de ítems del pedido

            # Verificar que el pedido tenga al menos un ítem.
            if not items:
                return Response({'error': 'El pedido no puede estar vacío'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear el pedido asociado al usuario.
            pedido = Pedido.objects.create(usuario_id=usuario_id)

            # Agregar ítems al pedido.
            for item in items:
                # Obtener el producto asociado al ítem.
                producto = Producto.objects.get(id=item.get('producto_id'))

                # Validar que la cantidad no exceda el stock disponible.
                if item.get('cantidad', 1) > producto.stock:
                    raise ValidationError(f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")

                # Crear el ítem de pedido.
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item.get('cantidad', 1),  # Cantidad por defecto es 1.
                    precio_unitario=producto.precio  # Precio unitario del producto.
                )

            # Calcular el total del pedido.
            pedido.calcular_total()

            # Retornar una respuesta exitosa con el ID del pedido creado.
            return Response({'mensaje': 'Pedido creado exitosamente', 'pedido_id': pedido.id}, status=status.HTTP_201_CREATED)
        except Producto.DoesNotExist:
            # Si el producto no existe, retornar un error 404.
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            # Si hay un error de validación, retornar un error 400.
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Si ocurre cualquier otro error, retornar un error 500 con el mensaje de la excepción.
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Si el método no es POST, retornar un error 405 (Método no permitido).
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Proteger la vista con autenticación
def listar_pedidos(request):
    """
    Vista para listar todos los pedidos de un usuario.
    """
    if request.method == 'GET':
        # Obtener el ID del usuario desde los parámetros de la URL.
        usuario_id = request.query_params.get('usuario_id')

        # Verificar que se haya proporcionado el ID del usuario.
        if not usuario_id:
            return Response({'error': 'Se requiere el ID del usuario'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los pedidos del usuario y optimizar las consultas con select_related y prefetch_related.
        pedidos = Pedido.objects.filter(usuario_id=usuario_id).select_related('usuario').prefetch_related('items')

        # Serializar los pedidos para convertirlos en JSON.
        serializer = PedidoSerializer(pedidos, many=True)

        # Retornar la lista de pedidos en formato JSON.
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Si el método no es GET, retornar un error 405 (Método no permitido).
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Proteger la vista con autenticación
def detalle_pedido(request, pedido_id):
    """
    Vista para obtener los detalles de un pedido específico.
    """
    try:
        # Obtener el pedido por su ID.
        pedido = Pedido.objects.get(id=pedido_id)

        # Serializar el pedido para convertirlo en JSON.
        serializer = PedidoSerializer(pedido)

        # Retornar los detalles del pedido en formato JSON.
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pedido.DoesNotExist:
        # Si el pedido no existe, retornar un error 404.
        return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Proteger la vista con autenticación
def actualizar_pedido(request, pedido_id):
    """
    Vista para actualizar un pedido (por ejemplo, cambiar el estado).
    """
    try:
        # Obtener el pedido por su ID.
        pedido = Pedido.objects.get(id=pedido_id)

        # Serializar el pedido con los datos proporcionados en el request.
        # `partial=True` permite actualizaciones parciales (no todos los campos son obligatorios).
        serializer = PedidoSerializer(pedido, data=request.data, partial=True)

        # Validar los datos proporcionados.
        if serializer.is_valid():
            # Guardar los cambios en el pedido.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Si los datos no son válidos, retornar un error 400 con los errores de validación.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Pedido.DoesNotExist:
        # Si el pedido no existe, retornar un error 404.
        return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Proteger la vista con autenticación
def cancelar_pedido(request, pedido_id):
    """
    Vista para cancelar un pedido.
    """
    try:
        # Obtener el pedido por su ID.
        pedido = Pedido.objects.get(id=pedido_id)

        # Cambiar el estado del pedido a 'cancelado'.
        pedido.estado = 'cancelado'  # Suponiendo que tienes un campo 'estado' en tu modelo.

        # Guardar los cambios en el pedido.
        pedido.save()

        # Retornar una respuesta exitosa.
        return Response({'mensaje': 'Pedido cancelado exitosamente'}, status=status.HTTP_200_OK)
    except Pedido.DoesNotExist:
        # Si el pedido no existe, retornar un error 404.
        return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)