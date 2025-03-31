from django.urls import path
from . import views

app_name = 'facturas'  # Namespace para referencias inversas

urlpatterns = [
    # Generación de factura (POST para creación, GET para descarga)
    path('pedidos/<int:pedido_id>/factura/', 
        views.generar_factura, 
        name='generar-factura'),
    
    # Listado completo de facturas
    path('facturas/', 
        views.listar_facturas, 
        name='listar-facturas'),
    
    # Detalle específico de factura (metadatos JSON)
    path('facturas/<int:factura_id>/', 
        views.detalle_factura, 
        name='detalle-factura'),
    
    # Descarga directa de PDF
    path('facturas/<int:factura_id>/descargar/', 
        views.descargar_factura_pdf, 
        name='descargar-factura')
]