# Este archivo define las rutas (URLs) para las vistas.
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]

# Mejoras sugeridas:
# 1. Agregar rutas para listar productos por categoría.
# 2. Usar Django REST Framework para simplificar la creación de APIs.
