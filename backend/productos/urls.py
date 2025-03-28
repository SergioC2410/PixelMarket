from django.urls import path
from .views import (
    ProductoListCreateAPIView,
    ProductoRetrieveUpdateDestroyAPIView,
    categoria_list,
    categoria_detail
)

urlpatterns = [
    # Productos (Vistas basadas en clases)
    path('productos/', ProductoListCreateAPIView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='producto-detail'),
    
    # Categorías (Vistas basadas en funciones con @api_view)
    path('categorias/', categoria_list, name='categoria-list'),
    path('categorias/<int:pk>/', categoria_detail, name='categoria-detail'),
]