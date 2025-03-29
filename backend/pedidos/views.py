"""
Vistas para la gestión de pedidos en el sistema e-commerce.
Conecta con las apps: usuarios, productos y facturas.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from productos.models import Producto
from usuarios.models import Usuario
from facturas.models import Factura  # Conexión con app facturas
from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer, ItemPedidoSerializer

# Constantes para mensajes de error
ERRORES = {
    'pedido_no_encontrado': 'Pedido no encontrado',
    'usuario_no_autorizado': 'No tienes permisos para esta acción',
    'stock_insuficiente': 'No hay suficiente stock para {producto}. Disponible: {stock}',
    'pedido_vacio': 'El pedido no puede estar vacío',
    'producto_no_existe': 'Producto con ID {id} no encontrado'
}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def crear_pedido(request):
    """
    Crea un nuevo pedido y genera la factura correspondiente.
    Requiere:
    - usuario_id: ID del usuario
    - items: Lista de items con producto_id y cantidad
    """
    try:
        data = request.data
        usuario_id = data.get('usuario_id')
        items = data.get('items', [])
        
        # Validación básica
        if not items:
            return Response({'error': ERRORES['pedido_vacio']}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que el usuario coincide con el token
        if request.user.id != int(usuario_id):
            return Response({'error': ERRORES['usuario_no_autorizado']}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Obtener usuario completo
        usuario = Usuario.objects.get(id=usuario_id)
        
        with transaction.atomic():
            # Crear pedido
            pedido = Pedido.objects.create(usuario=usuario)
            
            # Procesar items
            for item in items:
                producto_id = item.get('producto_id')
                cantidad = item.get('cantidad', 1)
                
                # Bloquear producto para evitar race conditions
                producto = Producto.objects.select_for_update().get(id=producto_id)
                
                # Validar stock
                if cantidad > producto.stock:
                    raise ValidationError(
                        ERRORES['stock_insuficiente'].format(
                            producto=producto.nombre,
                            stock=producto.stock
                        )
                    )
                
                # Crear item de pedido
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                
                # Actualizar stock
                producto.stock -= cantidad
                producto.save()
            
            # Calcular total
            pedido.calcular_total()
            
            # Generar factura (conexión con app facturas)
            factura = Factura.objects.create(
                pedido=pedido,
                usuario=usuario,
                total=pedido.total,
                estado='pendiente'
            )
            
            return Response({
                'mensaje': 'Pedido creado exitosamente',
                'pedido_id': pedido.id,
                'factura_id': factura.id
            }, status=status.HTTP_201_CREATED)
            
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, 
                      status=status.HTTP_404_NOT_FOUND)
    except Producto.DoesNotExist:
        return Response({'error': ERRORES['producto_no_existe'].format(id=producto_id)}, 
                      status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({'error': str(e)}, 
                      status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Error inesperado: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_pedidos(request):
    """
    Lista todos los pedidos del usuario autenticado.
    Incluye los items de cada pedido.
    """
    try:
        # Solo pedidos del usuario actual
        pedidos = Pedido.objects.filter(
            usuario=request.user
        ).select_related('usuario').prefetch_related(
            'items__producto'
        ).order_by('-fecha_creacion')
        
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_pedido(request, pedido_id):
    """
    Obtiene los detalles de un pedido específico.
    Verifica que el pedido pertenezca al usuario.
    """
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Verificar propiedad del pedido
        if pedido.usuario != request.user:
            return Response({'error': ERRORES['usuario_no_autorizado']}, 
                          status=status.HTTP_403_FORBIDDEN)
            
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Pedido.DoesNotExist:
        return Response({'error': ERRORES['pedido_no_encontrado']}, 
                      status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def actualizar_estado_pedido(request, pedido_id):
    """
    Actualiza el estado de un pedido (solo admin o dueño).
    Estados permitidos: pendiente, completado, cancelado
    """
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Verificar permisos
        if pedido.usuario != request.user and not request.user.is_staff:
            return Response({'error': ERRORES['usuario_no_autorizado']}, 
                          status=status.HTTP_403_FORBIDDEN)
            
        nuevo_estado = request.data.get('estado')
        
        # Validar estado
        if nuevo_estado not in dict(Pedido.ESTADOS).keys():
            return Response({'error': f"Estado inválido. Use: {', '.join(dict(Pedido.ESTADOS).keys())}"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar estado
        pedido.estado = nuevo_estado
        pedido.save()
        
        # Si se cancela, devolver stock
        if nuevo_estado == 'cancelado':
            with transaction.atomic():
                for item in pedido.items.all():
                    producto = item.producto
                    producto.stock += item.cantidad
                    producto.save()
        
        return Response(PedidoSerializer(pedido).data, 
                      status=status.HTTP_200_OK)
        
    except Pedido.DoesNotExist:
        return Response({'error': ERRORES['pedido_no_encontrado']}, 
                      status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factura_por_pedido(request, pedido_id):
    """
    Obtiene la factura asociada a un pedido
    (Conectado con app facturas)
    """
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Verificar propiedad del pedido
        if pedido.usuario != request.user and not request.user.is_staff:
            return Response({'error': ERRORES['usuario_no_autorizado']}, 
                          status=status.HTTP_403_FORBIDDEN)
            
        factura = Factura.objects.get(pedido=pedido)
        return Response({
            'factura_id': factura.id,
            'numero_factura': factura.numero,
            'total': factura.total,
            'estado': factura.estado,
            'fecha_emision': factura.fecha_emision
        }, status=status.HTTP_200_OK)
        
    except Pedido.DoesNotExist:
        return Response({'error': ERRORES['pedido_no_encontrado']}, 
                      status=status.HTTP_404_NOT_FOUND)
    except Factura.DoesNotExist:
        return Response({'error': 'Factura no encontrada para este pedido'}, 
                      status=status.HTTP_404_NOT_FOUND)