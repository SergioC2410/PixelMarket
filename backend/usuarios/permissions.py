from rest_framework import permissions

class EsPropietario(permissions.BasePermission):
    """
    Permiso personalizado para verificar que el usuario autenticado es dueño del recurso.
    Versión mejorada con:
    - Soporte para múltiples tipos de relaciones (FK, OneToOne, etc.)
    - Mensajes de error más descriptivos
    - Compatibilidad con vistas genéricas y personalizadas
    """
    
    message = 'No tienes permisos para realizar esta acción sobre un recurso que no te pertenece.'

    def has_permission(self, request, view):
        # Permite acceso a listados (GET) o creación (POST)
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # Verifica relaciones comunes en los modelos
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'comprador'):
            return obj.comprador == request.user
        
        # Para modelos que tienen relación directa con el usuario
        return obj == request.user