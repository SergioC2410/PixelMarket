# Este archivo define las rutas (URLs) para las vistas.


from django.urls import path
from . import views

urlpatterns = [
    path('facturas/generar/<int:pedido_id>/', views.generar_factura, name='generar_factura'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
]

# Mejoras sugeridas:
# 1. Agregar rutas para descargar facturas en diferentes formatos (ej: JSON, CSV).
# 2. Usar Django REST Framework para simplificar la creación de APIs.