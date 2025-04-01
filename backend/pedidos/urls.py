from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PedidoViewSet,
    PedidoListCreateView,
    PedidoDetailView,
    cancelar_pedido,
    marcar_como_pagado,
    reembolsar_pedido
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('pedidos/crear/', PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedidos/<int:pk>/cancelar/', cancelar_pedido, name='pedido-cancelar'),
    path('pedidos/<int:pk>/marcar-como-pagado/', marcar_como_pagado, name='pedido-marcar-como-pagado'),
    path('pedidos/<int:pk>/reembolsar/', reembolsar_pedido, name='pedido-reembolsar'),
] + router.urls