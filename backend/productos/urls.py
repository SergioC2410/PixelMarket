from django.urls import path
from . import views
from .views import (
    ProductoListCreateAPIView,
    ProductoRetrieveUpdateDestroyAPIView,
    categoria_list,
    categoria_detail,
    MisProductosListAPIView  # Nueva vista importada
)

urlpatterns = [
    # =============================================
    # Endpoints de Productos (APIViews)
    # =============================================
    path('productos/', ProductoListCreateAPIView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='producto-detail'),
    
    # Nuevo endpoint para productos del usuario autenticado
    path('productos/mis-productos/', MisProductosListAPIView.as_view(), name='mis-productos'),
    
    # =============================================
    # Endpoints de Categorías (Funciones)
    # =============================================
    path('categorias/', categoria_list, name='categoria-list'),
    path('categorias/<int:pk>/', categoria_detail, name='categoria-detail'),
    
    # =============================================
    # Nuevos endpoints filtrados por usuario (Opcionales)
    # =============================================
    path('productos/vendedor/<int:vendedor_id>/', 
         ProductoListCreateAPIView.as_view(), 
         name='productos-por-vendedor'),
]