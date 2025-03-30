"""
Configuración de URLs para la app de pedidos.

Define todas las rutas API relacionadas con:
- Creación y gestión de pedidos
- Items de pedido
- Acciones especiales (cancelar, generar factura, etc.)

Conecta con:
- Vistas locales de pedidos (views.py)
- Sistema de autenticación de Django REST Framework
- Apps relacionadas (facturas, usuarios, productos)
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Configuración para documentación automática (Swagger/OpenAPI)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Deshabilitar documentación Swagger para ciertas vistas (opcional)
disable_swagger = swagger_auto_schema(auto_schema=None)

# Router para vistas basadas en ViewSets (si las hubiera)
# router = DefaultRouter()
# router.register(r'pedidos', views.PedidoViewSet, basename='pedido')

urlpatterns = [
    # ---------------------------------------------------------------
    # Endpoints básicos de pedidos
    # ---------------------------------------------------------------
    
    path(
        'api/pedidos/',
        views.listar_pedidos,
        name='pedido-list',
    ),
    
    path(
        'api/pedidos/crear/',
        swagger_auto_schema(
            method='post',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['items_data'],
                properties={
                    'items_data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'producto': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'cantidad': openapi.Schema(type=openapi.TYPE_INTEGER),
                            }
                        )
                    )
                }
            ),
            responses={
                201: 'Pedido creado exitosamente',
                400: 'Datos inválidos o falta stock',
                403: 'No autenticado'
            }
        )(views.crear_pedido),
        name='pedido-create',
    ),
    
    # ---------------------------------------------------------------
    # Endpoints específicos por pedido
    # ---------------------------------------------------------------
    
    path(
        'api/pedidos/<int:pedido_id>/',
        views.detalle_pedido,
        name='pedido-detail',
    ),
    
    path(
        'api/pedidos/<int:pedido_id>/actualizar/',
        swagger_auto_schema(
            method='put',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'estado': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=[estado[0] for estado in views.Pedido.ESTADOS]
                    ),
                    'items_data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'producto': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'cantidad': openapi.Schema(type=openapi.TYPE_INTEGER),
                            }
                        )
                    )
                }
            ),
            responses={
                200: 'Pedido actualizado',
                400: 'Datos inválidos',
                403: 'No autorizado',
                404: 'Pedido no encontrado'
            }
        )(views.actualizar_pedido),
        name='pedido-update',
    ),
    
    path(
        'api/pedidos/<int:pedido_id>/cancelar/',
        swagger_auto_schema(
            method='post',
            responses={
                200: 'Pedido cancelado',
                403: 'No autorizado',
                404: 'Pedido no encontrado',
                400: 'Pedido ya cancelado'
            }
        )(views.cancelar_pedido),
        name='pedido-cancel',
    ),
    
    # ---------------------------------------------------------------
    # Endpoints de facturación (conexión con app facturas)
    # ---------------------------------------------------------------
    
    path(
        'api/pedidos/<int:pedido_id>/factura/',
        swagger_auto_schema(
            method='get',
            responses={
                200: 'Detalles de factura',
                403: 'No autorizado',
                404: 'No encontrado'
            }
        )(views.factura_por_pedido),
        name='pedido-factura',
    ),
    
    path(
        'api/pedidos/<int:pedido_id>/generar-factura/',
        swagger_auto_schema(
            method='post',
            responses={
                201: 'Factura generada',
                400: 'Factura ya existe',
                403: 'No autorizado',
                404: 'Pedido no encontrado'
            }
        )(views.generar_factura),
        name='generar-factura',
    ),
    
    # ---------------------------------------------------------------
    # Endpoints adicionales
    # ---------------------------------------------------------------
    
    path(
        'api/pedidos/usuario/<int:usuario_id>/',
        swagger_auto_schema(
            method='get',
            manual_parameters=[
                openapi.Parameter(
                    'estado',
                    openapi.QUERY,
                    description="Filtrar por estado",
                    type=openapi.TYPE_STRING,
                    enum=[estado[0] for estado in views.Pedido.ESTADOS]
                )
            ],
            responses={
                200: 'Lista de pedidos del usuario',
                403: 'No autorizado',
                404: 'Usuario no encontrado'
            }
        )(views.pedidos_por_usuario),
        name='user-pedidos',
    ),
    
    path(
        'api/pedidos/<int:pedido_id>/items/',
        swagger_auto_schema(
            method='get',
            responses={
                200: 'Lista de items del pedido',
                403: 'No autorizado',
                404: 'Pedido no encontrado'
            }
        )(views.items_por_pedido),
        name='pedido-items',
    ),
]

# Si se usara ViewSets (opcional)
# urlpatterns += router.urls