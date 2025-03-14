# Este archivo define el modelo de la base de datos para los usuarios.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    Aquí puedes agregar campos adicionales según las necesidades del proyecto.
    """
    ROLES = (
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='comprador')
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Campo adicional
    direccion = models.TextField(blank=True, null=True)  # Campo adicional

    def __str__(self):
        """
        Representación en cadena del usuario (aparece en el panel de administración).
        """
        return self.username

    # Mejoras sugeridas:
    # 1. Agregar validaciones personalizadas (ej: formato de teléfono).
    # 2. Implementar métodos útiles, como `es_vendedor()` o `es_comprador()`.