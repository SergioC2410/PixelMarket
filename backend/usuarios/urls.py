# Este archivo define las rutas (URLs) para las vistas
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
]

# Mejoras sugeridas:
# 1. Agregar rutas para actualizar y eliminar usuarios.
# 2. Usar Django REST Framework para simplificar la creación de APIs.