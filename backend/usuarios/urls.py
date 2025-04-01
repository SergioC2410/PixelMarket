from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# URLs base de la API
urlpatterns = [
    # ======================
    # 1. Autenticación
    # ======================
    path('auth/', include([
        path('registro/', views.registro_usuario, name='registro_usuario'),
        path('login/', views.iniciar_sesion, name='iniciar_sesion'),
        path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),

    # ======================
    # 2. Usuarios
    # ======================
    path('usuarios/', include([
        path('perfil/', views.obtener_perfil_completo, name='perfil_completo'),
        path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
        path('perfil/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),
        path('ubicacion/', views.gestionar_ubicacion, name='gestion_ubicacion'),
        path('metodos-pago/', include([
            path('', views.lista_metodos_pago, name='lista_metodos_pago'),
            path('<int:pk>/', views.detalle_metodo_pago, name='detalle_metodo_pago'),
        ])),
    ])),

    # ======================
    # 3. Productos (API externa)
    # ======================
    path('productos/', include('productos.urls')),  # Asume que existe productos/urls.py

    # ======================
    # 4. Pedidos (API externa)
    # ======================
    path('pedidos/', include('pedidos.urls')),  # Asume que existe pedidos/urls.py

    # ======================
    # 5. Carrito (Si lo implementas)
    # ======================
    # path('carrito/', include(...)), 
]