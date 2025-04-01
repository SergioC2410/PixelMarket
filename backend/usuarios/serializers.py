from rest_framework import serializers
from .models import Usuario, Ubicacion, MetodoPago
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

# ----------------------------
# Validadores personalizados (Mejorados)
# ----------------------------
def validar_formato_telefono(value):
    """Valida formato +58XXXXXXXXXX con mensaje descriptivo"""
    if not re.match(r'^\+58\d{10}$', value):
        raise ValidationError(
            "El teléfono debe comenzar con +58 seguido de 10 dígitos. Ej: +584121234567"
        )

def validar_cedula_venezolana(value):
    """Valida longitud y formato numérico"""
    if not value.isdigit():
        raise ValidationError("La cédula solo debe contener dígitos numéricos.")
    if len(value) < 6 or len(value) > 8:
        raise ValidationError("La cédula debe tener entre 6 y 8 dígitos.")

# ----------------------------
# Serializadores principales
# ----------------------------
class UsuarioBaseSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    telefono = serializers.CharField(
        validators=[validar_formato_telefono],
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'first_name', 'last_name', 'nombre_completo',
            'telefono', 'cedula', 'fecha_registro'
        ]
        read_only_fields = ['fecha_registro']
        extra_kwargs = {
            'cedula': {'write_only': True}  # Ocultar en respuestas
        }

    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirmar contraseña"
    )
    telefono = serializers.CharField(
        validators=[validar_formato_telefono],
        help_text="Formato: +58XXXXXXXXXX"
    )
    cedula = serializers.CharField(
        validators=[validar_cedula_venezolana],
        help_text="6-8 dígitos sin puntos ni guiones"
    )

    class Meta:
        model = Usuario
        fields = [
            'email', 'password', 'password2', 
            'telefono', 'cedula', 'first_name', 'last_name'
        ]
        extra_kwargs = {
            'first_name': {'required': True, 'help_text': "Mínimo 2 caracteres"},
            'last_name': {'required': True, 'help_text': "Mínimo 2 caracteres"}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."},
                code='password_mismatch'
            )
        
        try:
            validate_email(data['email'])
        except ValidationError:
            raise serializers.ValidationError(
                {"email": "Ingrese un correo electrónico válido."},
                code='invalid_email'
            )

        data.pop('password2')
        return data

    def create(self, validated_data):
        return Usuario.objects.create_user(
            password=validated_data.pop('password'),
            **validated_data
        )

class UsuarioActualizacionSerializer(UsuarioBaseSerializer):
    class Meta(UsuarioBaseSerializer.Meta):
        extra_kwargs = {
            'email': {'read_only': True},
            'cedula': {'read_only': True},
            'telefono': {'required': False}
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
        validators=[validar_formato_telefono],
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