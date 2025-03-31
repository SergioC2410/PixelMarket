from django.urls import path
from . import views

app_name = 'facturas'

urlpatterns = [
    path('generar/<int:pedido_id>/', views.generar_factura, name='generar-factura'),
    path('', views.listar_facturas, name='lista-facturas'),
    path('<int:factura_id>/', views.detalle_factura, name='detalle-factura'),
    path('<int:factura_id>/descargar/', views.descargar_factura_pdf, name='descargar-factura'),
]