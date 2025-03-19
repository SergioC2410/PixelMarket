# Importamos los módulos necesarios de Django y Django REST Framework (DRF)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer, ProductoUpdateSerializer
import json
from django.core.paginator import Paginator
from django.db.models import Q

# Definir constantes
ERROR_METODO_NO_PERMITIDO = 'Método no permitido'

# Vista para listar todos los productos
@csrf_exempt
def listar_productos(request):
    """
    Vista para listar todos los productos.
    Soporta paginación, filtrado por categoría, precio y búsqueda por nombre/descripción.
    """
    if request.method == 'GET':
        # Filtros
        categoria_id = request.GET.get('categoria_id')
        precio_min = request.GET.get('precio_min')
        precio_max = request.GET.get('precio_max')
        search_query = request.GET.get('q')

        # Consulta base
        productos = Producto.objects.all()

        # Aplicar filtros
        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)
        if precio_min:
            productos = productos.filter(precio__gte=precio_min)
        if precio_max:
            productos = productos.filter(precio__lte=precio_max)
        if search_query:
            productos = productos.filter(Q(nombre__icontains=search_query) | Q(descripcion__icontains=search_query))

        # Paginación
        paginator = Paginator(productos, 10)  # 10 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Serializar productos
        serializer = ProductoSerializer(page_obj, many=True)
        return JsonResponse({
            'productos': serializer.data,
            'total_paginas': paginator.num_pages
        }, safe=False)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

# Vista para crear un nuevo producto
@csrf_exempt
def crear_producto(request):
    """
    Vista para crear un nuevo producto.
    Valida los datos y asocia el producto a una categoría.
    """
    if request.method == 'POST':
        try:
            # Cargar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Validar y crear el producto usando el serializador
            serializer = ProductoSerializer(data=data, context={'categoria_id': data.get('categoria_id')})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

# Vista para actualizar un producto existente
@csrf_exempt
def actualizar_producto(request, producto_id):
    """
    Vista para actualizar un producto existente.
    Soporta actualización parcial (PATCH) y completa (PUT).
    """
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            # Obtener el producto a actualizar
            producto = Producto.objects.get(id=producto_id)

            # Cargar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Usar el serializador de actualización parcial para PATCH
            if request.method == 'PATCH':
                serializer = ProductoUpdateSerializer(producto, data=data, partial=True)
            else:  # PUT
                serializer = ProductoSerializer(producto, data=data)

            # Validar y guardar los cambios
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

# Vista para eliminar un producto
@csrf_exempt
def eliminar_producto(request, producto_id):
    """
    Vista para eliminar un producto.
    """
    if request.method == 'DELETE':
        try:
            # Obtener el producto a eliminar
            producto = Producto.objects.get(id=producto_id)

            # Eliminar el producto
            producto.delete()
            return JsonResponse({'mensaje': 'Producto eliminado exitosamente'}, status=200)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

# Vista para listar productos por categoría
@csrf_exempt
def listar_productos_por_categoria(request, categoria_id):
    """
    Vista para listar todos los productos de una categoría específica.
    """
    if request.method == 'GET':
        try:
            # Obtener la categoría
            categoria = Categoria.objects.get(id=categoria_id)

            # Obtener todos los productos de la categoría
            productos = categoria.productos.all()

            # Serializar los productos
            serializer = ProductoSerializer(productos, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Categoria.DoesNotExist:
            return JsonResponse({'error': 'Categoría no encontrada'}, status=404)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

# Vistas para categorías
@csrf_exempt
def listar_categorias(request):
    """
    Vista para listar todas las categorías.
    """
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

@csrf_exempt
def crear_categoria(request):
    """
    Vista para crear una nueva categoría.
    """
    if request.method == 'POST':
        try:
            # Cargar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Crear la categoría
            categoria = Categoria.objects.create(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', '')
            )

            # Serializar la categoría
            serializer = CategoriaSerializer(categoria)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

@csrf_exempt
def detalle_categoria(request, categoria_id):
    """
    Vista para obtener los detalles de una categoría específica.
    """
    if request.method == 'GET':
        categoria = get_object_or_404(Categoria, id=categoria_id)
        serializer = CategoriaSerializer(categoria)
        return JsonResponse(serializer.data)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

@csrf_exempt
def actualizar_categoria(request, categoria_id):
    """
    Vista para actualizar una categoría existente.
    """
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            # Obtener la categoría a actualizar
            categoria = get_object_or_404(Categoria, id=categoria_id)

            # Cargar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Actualizar los campos de la categoría
            categoria.nombre = data.get('nombre', categoria.nombre)
            categoria.descripcion = data.get('descripcion', categoria.descripcion)
            categoria.save()

            # Serializar la categoría actualizada
            serializer = CategoriaSerializer(categoria)
            return JsonResponse(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)

@csrf_exempt
def eliminar_categoria(request, categoria_id):
    """
    Vista para eliminar una categoría.
    """
    if request.method == 'DELETE':
        try:
            # Obtener la categoría a eliminar
            categoria = get_object_or_404(Categoria, id=categoria_id)

            # Eliminar la categoría
            categoria.delete()
            return JsonResponse({'mensaje': 'Categoría eliminada correctamente'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': ERROR_METODO_NO_PERMITIDO}, status=405)