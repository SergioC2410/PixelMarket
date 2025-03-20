from django.urls import path
from . import views

urlpatterns = [
    path('facturas/generar/<int:pedido_id>/', views.generar_factura, name='generar_factura'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    path('facturas/<int:factura_id>/descargar/pdf/', views.descargar_factura_pdf, name='descargar_factura_pdf'), #Se puede usar cualquier formato, XML, JSON o PDF
    #Se puede implementar cualquier formato en un futuro
]