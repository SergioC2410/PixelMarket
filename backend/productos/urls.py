from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Usamos DefaultRouter de DRF para manejar las rutas de las vistas basadas en clases
router = DefaultRouter()

# Aquí podrías agregar otras rutas de vistas basadas en clases (si las tienes),
# por ejemplo, si tienes un ViewSet para los productos:
# router.register(r'productos', views.ProductoViewSet, basename='producto')

urlpatterns = [
    # Rutas para manejar productos
    # Ruta para crear un nuevo producto (incluye imagen)
    path('productos/crear/', views.crear_producto, name='crear_producto'),

    # Ruta para listar todos los productos
    path('productos/', views.listar_productos, name='listar_productos'),

    # Ruta para obtener los detalles de un producto específico
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Ruta para actualizar un producto (incluyendo la imagen)
    path('productos/<int:producto_id>/actualizar/', views.actualizar_producto, name='actualizar_producto'),

    # Ruta para eliminar un producto
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    # Rutas para manejar pedidos (puedes agregar esto si tienes una funcionalidad de pedidos)
    # Ruta para crear un nuevo pedido
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),

    # Ruta para listar todos los pedidos
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),

    # Ruta para obtener detalles de un pedido específico
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    # Ruta para actualizar un pedido (por ejemplo, cambiar el estado)
    path('pedidos/<int:pedido_id>/actualizar/', views.actualizar_pedido, name='actualizar_pedido'),

    # Ruta para cancelar un pedido
    path('pedidos/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
]

# Agregamos las rutas generadas por el router para las vistas basadas en clases
urlpatterns += router.urls

# Configuración para servir archivos estáticos y de medios en desarrollo
# Esto permite que las imágenes y otros archivos sean accesibles a través de URLs
from django.conf import settings
from django.conf.urls.static import static

# Agregamos las rutas para servir archivos de medios (como las imágenes de los productos)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
