# Este archivo contiene la lógica para manejar las solicitudes HTTP (APIs).


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, Categoria
import json

@csrf_exempt
def listar_productos(request):
    """
    Vista para listar todos los productos.
    """
    if request.method == 'GET':
        productos = Producto.objects.all()
        productos_data = [{
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'categoria': producto.categoria.nombre,
            'stock': producto.stock
        } for producto in productos]
        return JsonResponse(productos_data, safe=False)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def crear_producto(request):
    """
    Vista para crear un nuevo producto.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            categoria = Categoria.objects.get(id=data.get('categoria_id'))
            producto = Producto.objects.create(
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                precio=data.get('precio'),
                categoria=categoria,
                stock=data.get('stock', 0)
            )
            return JsonResponse({'mensaje': 'Producto creado exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def actualizar_producto(request, producto_id):
    """
    Vista para actualizar un producto existente.
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            producto = Producto.objects.get(id=producto_id)
            producto.nombre = data.get('nombre', producto.nombre)
            producto.descripcion = data.get('descripcion', producto.descripcion)
            producto.precio = data.get('precio', producto.precio)
            producto.stock = data.get('stock', producto.stock)
            producto.save()
            return JsonResponse({'mensaje': 'Producto actualizado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_producto(request, producto_id):
    """
    Vista para eliminar un producto.
    """
    if request.method == 'DELETE':
        try:
            producto = Producto.objects.get(id=producto_id)
            producto.delete()
            return JsonResponse({'mensaje': 'Producto eliminado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Mejoras sugeridas:
# 1. Agregar paginación para la lista de productos.
# 2. Implementar búsqueda y filtrado (ej: por categoría, precio).
# 3. Agregar pruebas unitarias para cada vista.