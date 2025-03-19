from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Usamos DefaultRouter de DRF para manejar las rutas de vistas basadas en clases si las tienes
router = DefaultRouter()

# Aquí puedes agregar vistas basadas en clases si las tienes, como un ViewSet para productos
# router.register(r'productos', views.ProductoViewSet, basename='producto')
# router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

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

    # Rutas para manejar categorías
    # Ruta para crear una nueva categoría
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),

    # Ruta para listar todas las categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),

    # Ruta para obtener los detalles de una categoría específica
    path('categorias/<int:categoria_id>/', views.detalle_categoria, name='detalle_categoria'),

    # Ruta para actualizar una categoría
    path('categorias/<int:categoria_id>/actualizar/', views.actualizar_categoria, name='actualizar_categoria'),

    # Ruta para eliminar una categoría
    path('categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
]

# Agregamos las rutas generadas por el router para las vistas basadas en clases (si las tienes)
urlpatterns += router.urls

# Configuración para servir archivos estáticos y de medios en desarrollo
# Esto permite que las imágenes y otros archivos sean accesibles a través de URLs
from django.conf import settings
from django.conf.urls.static import static

# Agregamos las rutas para servir archivos de medios (como las imágenes de los productos)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
