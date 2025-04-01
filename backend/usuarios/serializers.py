from rest_framework import serializers
from .models import Usuario, Ubicacion, MetodoPago
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

# ----------------------------
# Serializadores para relaciones (Mejorados)
# ----------------------------
class UbicacionSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(
        source='get_estado_display', 
        read_only=True,
        help_text="Nombre legible del estado"
    )

    class Meta:
        model = Ubicacion
        fields = [
            'id', 'estado', 'estado_nombre', 
            'municipio', 'parroquia', 'direccion_exacta'
        ]
        extra_kwargs = {
            'usuario': {'read_only': True},
            'municipio': {'help_text': "Ej: Libertador, Chacao"},
            'parroquia': {'help_text': "Ej: El Recreo, La Candelaria"}
        }

class MetodoPagoSerializer(serializers.ModelSerializer):
    tipo_nombre = serializers.CharField(
        source='get_tipo_display', 
        read_only=True,
        help_text="Tipo de método de pago"
    )
    banco_nombre = serializers.CharField(
        source='get_banco_pago_movil_display', 
        read_only=True,
        help_text="Nombre del banco (solo Pago Móvil)"
    )
    email_binance = serializers.EmailField(
        required=False,
        help_text="Email asociado a Binance"
    )
    telefono_pago_movil = serializers.CharField(
        required=False,
        help_text="Formato: +58XXXXXXXXXX"
    )

    class Meta:
        model = MetodoPago
        fields = [
            'id', 'tipo', 'tipo_nombre', 'activo',
            'email_zelle', 'telefono_zelle',
            'email_binance',
            'banco_pago_movil', 'banco_nombre', 
            'telefono_pago_movil', 'cedula_pago_movil'
        ]
        read_only_fields = ['usuario']
        extra_kwargs = {
            'banco_pago_movil': {'help_text': "Código de 4 dígitos del banco"},
            'cedula_pago_movil': {'help_text': "Cédula asociada al Pago Móvil"}
        }

    def validate(self, data):
        tipo = data.get('tipo')
        request = self.context.get('request')
        
        # Validar campos requeridos
        if tipo == 'ZELLE' and not data.get('email_zelle'):
            raise serializers.ValidationError(
                {"email_zelle": "Requerido para Zelle."},
                code='zelle_required'
            )
        
        if tipo == 'PAGO_MOVIL' and not data.get('banco_pago_movil'):
            raise serializers.ValidationError(
                {"banco_pago_movil": "Requerido para Pago Móvil."},
                code='banco_required'
            )
        
        # Validar unicidad (solo en creación)
        if request and not self.instance and MetodoPago.objects.filter(
            usuario=request.user, 
            tipo=tipo, 
            activo=True
        ).exists():
            raise serializers.ValidationError(
                {"tipo": f"Ya tienes un método {tipo} activo."},
                code='metodo_duplicado'
            )
        
        return data

# ----------------------------
# Serializador detallado (Opcional mejorado)
# ----------------------------
class UsuarioDetalleSerializer(UsuarioBaseSerializer):
    ubicacion = UbicacionSerializer(
        read_only=True,
        help_text="Detalles de ubicación registrados"
    )
    metodos_pago = serializers.SerializerMethodField()

    class Meta(UsuarioBaseSerializer.Meta):
        fields = UsuarioBaseSerializer.Meta.fields + ['ubicacion', 'metodos_pago']
    
    def get_metodos_pago(self, obj):
        return MetodoPagoSerializer(
            obj.metodos_pago.filter(activo=True),
            many=True,
            context=self.context
        ).data      
        