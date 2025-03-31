"""
URL configuration for backend project.

Incluye:
- Panel de administración
- Endpoints API para productos, pedidos, usuarios y facturas
- Configuración para archivos media en desarrollo
- Documentación automática de API (Swagger/Redoc)
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

def home(request):
    """Endpoint raíz que muestra información básica de la API"""
    api_info = {
        "mensaje": "Bienvenido a la API de PixelMarket",
        "endpoints": {
            "admin": "/admin/",
            "api_docs": "/api/docs/",
            "productos": "/api/productos/",
            "pedidos": "/api/pedidos/",
            "usuarios": "/api/usuarios/",
            "facturas": "/api/facturas/"
        },
        "version": "1.0.0"
    }
    return JsonResponse(api_info, status=200)

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    

    # Apps principales
    path('api/', include('productos.urls')),
    path('api/', include('pedidos.urls')),
    path('api/', include('usuarios.urls')),
    path('api/', include('facturas.urls')),
    
    # Health Check
    path('health/', lambda r: JsonResponse({"status": "ok"})),
    
    # Página raíz
    path('', home, name='home'),
]

# Configuraciones para entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)