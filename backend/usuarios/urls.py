# Este archivo define las rutas (URLs) para las vistas de la aplicación de usuarios.
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Rutas para autenticación y gestión de usuarios
    path('registro/', views.registro_usuario, name='registro_usuario'),  # Registrar un nuevo usuario
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),  # Iniciar sesión
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),  # Cerrar sesión

    # Rutas para obtener y gestionar información del usuario
    path('info-usuario/', views.obtener_info_usuario, name='obtener_info_usuario'),  # Obtener información del usuario autenticado
    path('actualizar-usuario/<int:user_id>/', views.actualizar_usuario, name='actualizar_usuario'),  # Actualizar usuario (PUT)
    path('actualizar-usuario-parcial/<int:user_id>/', views.actualizar_usuario_parcial, name='actualizar_usuario_parcial'),  # Actualización parcial (PATCH)
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),  # Eliminar usuario

    # Rutas para JWT (JSON Web Tokens)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token de acceso
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar token de acceso
]

# Mejoras adicionales:
# 1. Agregar protección de rutas con permisos (por ejemplo, solo usuarios autenticados pueden acceder a ciertas rutas).
# 2. Usar Django REST Framework (DRF) para simplificar la creación de APIs.
# 3. Agregar documentación automática de APIs usando herramientas como Swagger o DRF Spectacular.