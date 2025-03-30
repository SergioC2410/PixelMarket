from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Usamos DefaultRouter de DRF para manejar las rutas de las vistas basadas en clases
router = DefaultRouter()

# Registramos las vistas basadas en clases (si las tienes)
# router.register(r'pedidos', views.PedidoViewSet, basename='pedido')

urlpatterns = [
    # Rutas para crear y listar pedidos
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),

    # Ruta para obtener detalles de un pedido específico
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    # Ruta para actualizar un pedido (por ejemplo, cambiar el estado)
    path('pedidos/<int:pedido_id>/actualizar/', views.actualizar_pedido, name='actualizar_pedido'),

    # Ruta para cancelar un pedido
    path('pedidos/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
]

# Agregamos las rutas generadas por el router
urlpatterns += router.urls