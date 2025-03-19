from django.urls import path
from . import views

urlpatterns = [
    # Rutas para productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('categorias/<int:categoria_id>/productos/', views.listar_productos_por_categoria, name='listar_productos_por_categoria'),

    # Rutas para categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),  # Listar todas las categorías
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),  # Crear una nueva categoría
    path('categorias/<int:categoria_id>/', views.detalle_categoria, name='detalle_categoria'),  # Detalles de una categoría
    path('categorias/<int:categoria_id>/actualizar/', views.actualizar_categoria, name='actualizar_categoria'),  # Actualizar una categoría
    path('categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),  # Eliminar una categoría
]