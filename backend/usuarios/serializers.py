# Este archivo es opcional, pero muy útil si usas Django REST Framework (DRF) para crear APIs.
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    Convierte objetos Usuario en JSON y viceversa.
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'telefono', 'direccion']
        extra_kwargs = {
            'password': {'write_only': True}  # La contraseña no se incluye en las respuestas
        }

    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.
        """
        usuario = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'comprador')
        )
        return usuario

# Mejoras sugeridas:
# 1. Agregar validaciones personalizadas (ej: formato de correo).
# 2. Implementar serializadores para actualización parcial (PATCH).