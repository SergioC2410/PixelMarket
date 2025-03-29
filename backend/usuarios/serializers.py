from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Serializador base para manejar datos generales del modelo Usuario
class UsuarioBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Campos que se incluirán en la serialización
        fields = ['id', 'email', 'first_name', 'last_name', 'telefono', 'cedula', 'fecha_registro']
        # Campos de solo lectura
        read_only_fields = ['fecha_registro']

# Serializador para el registro de nuevos usuarios
class UsuarioRegistroSerializer(serializers.ModelSerializer):
    # Campo para la contraseña, con validación y estilo de entrada
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    # Campo para confirmar la contraseña
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirmar contraseña"
    )

    class Meta:
        model = Usuario
        # Campos requeridos para el registro
        fields = ['email', 'password', 'password2', 'telefono', 'cedula', 'first_name', 'last_name']
        # Configuración adicional para campos específicos
        extra_kwargs = {
            'cedula': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    # Validaciones personalizadas
    def validate(self, data):
        # Validar que las contraseñas coincidan
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."},
                code='password_mismatch'
            )

        # Validar que el correo electrónico sea válido
        try:
            validate_email(data['email'])
        except ValidationError:
            raise serializers.ValidationError(
                {"email": "Ingrese un correo electrónico válido."},
                code='invalid_email'
            )

        # Validar que la cédula contenga solo números
        cedula = data.get('cedula', '')
        if not cedula.isdigit():
            raise serializers.ValidationError(
                {"cedula": "La cédula debe contener solo números."},
                code='invalid_cedula'
            )
        # Validar la longitud de la cédula
        if len(cedula) < 7 or len(cedula) > 20:
            raise serializers.ValidationError(
                {"cedula": "La cédula debe tener entre 7 y 20 dígitos."},
                code='invalid_cedula_length'
            )

        # Eliminar el campo password2 antes de devolver los datos validados
        data.pop('password2', None)
        return data

    # Método para crear un nuevo usuario
    def create(self, validated_data):
        # Extraer y eliminar la contraseña de los datos validados
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Asegurarse de que password2 no esté presente

        # Crear el usuario utilizando el método create_user del modelo Usuario
        usuario = Usuario.objects.create_user(
            password=password,
            **validated_data
        )
        return usuario

# Serializador para actualizar datos de un usuario existente
class UsuarioActualizacionSerializer(UsuarioBaseSerializer):
    class Meta(UsuarioBaseSerializer.Meta):
        # Configuración adicional para campos de solo lectura
        extra_kwargs = {
            'email': {'read_only': True},  # El correo no puede ser modificado
            'cedula': {'read_only': True},  # La cédula no puede ser modificada
        }
