from rest_framework import serializers  # Importa el módulo de serializadores de Django REST Framework
from .models import Usuario  # Importa el modelo Usuario definido en models.py
from django.core.exceptions import ValidationError  # Importa la excepción ValidationError para manejar errores de validación
from django.core.validators import validate_email  # Importa la función validate_email para validar el formato de un correo electrónico

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    """
    class Meta:
        model = Usuario  # Especifica el modelo que se va a serializar
        fields = ['id', 'username', 'email', 'rol', 'telefono', 'direccion', 'cedula', 'fecha_registro']  # Campos que se incluirán en la serialización
        extra_kwargs = {
            'password': {'write_only': True},  # La contraseña no se incluye en las respuestas
            'cedula': {'required': True},  # La cédula es obligatoria
        }

    def validate_email(self, value):
        """
        Valida que el correo electrónico tenga un formato válido.
        """
        try:
            validate_email(value)  # Valida el formato del correo electrónico
        except ValidationError:
            raise serializers.ValidationError("Correo electrónico inválido")  # Lanza un error de validación si el formato es incorrecto
        return value  # Devuelve el valor del correo electrónico si es válido

    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.
        """
        usuario = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'comprador'),  # Obtiene el rol del diccionario validado, por defecto 'comprador'
            telefono=validated_data.get('telefono', None),  # Obtiene el teléfono del diccionario validado, por defecto None
            direccion=validated_data.get('direccion', None),  # Obtiene la dirección del diccionario validado, por defecto None
            cedula=validated_data.get('cedula', '00000000')  # Obtiene la cédula del diccionario validado, por defecto '00000000'
        )
        return usuario  # Devuelve la instancia del usuario creado

    def update(self, instance, validated_data):
        """
        Actualiza un usuario existente con los datos validados.
        Permite la actualización parcial (PATCH).
        """
        instance.username = validated_data.get('username', instance.username)  # Actualiza el nombre de usuario si está presente en los datos validados
        instance.email = validated_data.get('email', instance.email)  # Actualiza el correo electrónico si está presente en los datos validados
        instance.rol = validated_data.get('rol', instance.rol)  # Actualiza el rol si está presente en los datos validados
        instance.telefono = validated_data.get('telefono', instance.telefono)  # Actualiza el teléfono si está presente en los datos validados
        instance.direccion = validated_data.get('direccion', instance.direccion)  # Actualiza la dirección si está presente en los datos validados
        instance.cedula = validated_data.get('cedula', instance.cedula)  # Actualiza la cédula si está presente en los datos validados
        instance.save()  # Guarda los cambios en la instancia del usuario
        return instance  # Devuelve la instancia del usuario actualizada

# Mejoras sugeridas:
# 1. Agregar validaciones personalizadas (ej: formato de correo).
# 2. Implementar serializadores para actualización parcial (PATCH).