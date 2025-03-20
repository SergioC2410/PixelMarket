from django.urls import path
from . import views  # Importa las vistas de la aplicación 'facturas'

# URL patterns para la aplicación de facturas
urlpatterns = [
    # Ruta para listar las facturas
    path('lista/', views.listar_facturas, name='lista_facturas'),

    # Ruta para generar una factura en PDF a partir de un pedido
    path('generar/<int:pedido_id>/', views.generar_factura, name='generar_factura'),

    # Ruta para descargar una factura específica en formato PDF
    path('descargar/<int:factura_id>/', views.descargar_factura_pdf, name='descargar_factura'),
]
