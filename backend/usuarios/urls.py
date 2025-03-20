# Este archivo define las rutas (URLs) para las vistas
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('info-usuario/', views.obtener_info_usuario, name='obtener_info_usuario'),  # Protegida en views.py
    path('actualizar-usuario/<int:user_id>/', views.actualizar_usuario, name='actualizar_usuario'),  # Ruta para actualizar usuario
    path('actualizar-usuario-parcial/<int:user_id>/', views.actualizar_usuario_parcial, name='actualizar_usuario_parcial'),  # Ruta para actualización parcial (PATCH)
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),  # Ruta para eliminar usuario
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar token
]

# Mejoras sugeridas:
# 1. Agregar rutas para actualizar y eliminar usuarios.
# 2. Usar Django REST Framework para simplificar la creación de APIs.