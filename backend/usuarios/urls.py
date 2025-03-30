from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Autenticación
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Solo mantener refresh
    
    # Gestión de perfil
    path('perfil/', views.obtener_info_usuario, name='perfil_usuario'),
    path('perfil/actualizar/', views.actualizar_usuario, name='actualizar_perfil'),
    
    # Eliminación (si realmente necesitas el ID en la URL)
    path('usuarios/<int:user_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
]