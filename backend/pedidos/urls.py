# Este archivo define las rutas (URLs) para las vistas.
from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
]

# Mejoras sugeridas:
# 1. Agregar rutas para actualizar y cancelar pedidos.
# 2. Usar Django REST Framework para simplificar la creación de APIs.