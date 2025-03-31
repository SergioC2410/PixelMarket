from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoListCreateAPIView,
    ProductoRetrieveUpdateDestroyAPIView,
    categoria_list,
    categoria_detail,
    ImagenProductoViewSet  # Nueva vista para imágenes
)

# Configurar el router para las imágenes de productos
router = DefaultRouter()
router.register(r'imagenes-producto', ImagenProductoViewSet, basename='imagen-producto')

urlpatterns = [
    # Productos (Vistas basadas en clases)
    path('productos/', ProductoListCreateAPIView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='producto-detail'),
    
    # Categorías (Vistas basadas en funciones con @api_view)
    path('categorias/', categoria_list, name='categoria-list'),
    path('categorias/<int:pk>/', categoria_detail, name='categoria-detail'),
    
    # Incluir las rutas del router
] + router.urls