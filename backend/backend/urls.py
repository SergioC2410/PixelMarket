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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuración para documentación API
schema_view = get_schema_view(
    openapi.Info(
        title="API PixelMarket",
        default_version='v1',
        description="Documentación de la API para el e-commerce PixelMarket",
        contact=openapi.Contact(email="soporte@pixelmarket.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    
    # Documentación API
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-redoc'),
    
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