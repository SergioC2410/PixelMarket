# Este archivo contiene la lógica para manejar las solicitudes HTTP (APIs).
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pedido, ItemPedido
from productos.models import Producto
import json

@csrf_exempt
def crear_pedido(request):
    """
    Vista para crear un nuevo pedido.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')
            items = data.get('items', [])  # Lista de ítems del pedido

            # Verificar que el pedido tenga al menos un ítem
            if not items:
                return JsonResponse({'error': 'El pedido no puede estar vacío'}, status=400)

            # Crear el pedido
            pedido = Pedido.objects.create(usuario_id=usuario_id)

            # Agregar ítems al pedido
            for item in items:
                producto = Producto.objects.get(id=item.get('producto_id'))
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item.get('cantidad', 1),
                    precio_unitario=producto.precio
                )

            return JsonResponse({'mensaje': 'Pedido creado exitosamente', 'pedido_id': pedido.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def listar_pedidos(request):
    """
    Vista para listar todos los pedidos de un usuario.
    """
    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        pedidos = Pedido.objects.filter(usuario_id=usuario_id)
        pedidos_data = [{
            'id': pedido.id,
            'fecha_creacion': pedido.fecha_creacion,
            'estado': pedido.estado,
            'total': str(pedido.total),
            'items': [{
                'producto': item.producto.nombre,
                'cantidad': item.cantidad,
                'precio_unitario': str(item.precio_unitario)
            } for item in pedido.items.all()]
        } for pedido in pedidos]
        return JsonResponse(pedidos_data, safe=False)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Mejoras sugeridas:
# 1. Agregar paginación para la lista de pedidos.
# 2. Implementar filtros (ej: por estado, fecha).
# 3. Agregar pruebas unitarias para cada vista.