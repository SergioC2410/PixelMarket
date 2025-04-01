from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from productos.models import Producto, Categoria
from usuarios.serializers import UsuarioBaseSerializer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 
            'nombre', 
            'descripcion', 
            'slug', 
            'imagen', 
            'activo',
            'orden',
            'visible',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = [
            'slug',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
        extra_kwargs = {
            'imagen': {'required': False},
            'orden': {'min_value': 0},
        }

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                _("El nombre de la categoría debe tener al menos 3 caracteres")
            )
        return value

class ProductoSerializer(serializers.ModelSerializer):
    # Campos relacionados
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        required=True,
        help_text=_("ID de la categoría a la que pertenece el producto")
    )
    
    vendedor = UsuarioBaseSerializer(read_only=True)
    
    # Campos calculados
    precio_final = serializers.SerializerMethodField(
        help_text=_("Precio con descuento aplicado")
    )
    
    # Validación de campos
    precio = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text=_("Precio base sin descuentos. Mínimo $0.01")
    )
    
    stock = serializers.IntegerField(
        min_value=0,
        help_text=_("Unidades disponibles en inventario. No puede ser negativo")
    )
    
    descuento = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Porcentaje de descuento (0-100%). 0 significa sin descuento")
    )

    class Meta:
        model = Producto
        fields = [
            'id', 
            'nombre', 
            'descripcion', 
            'precio', 
            'precio_final',
            'categoria', 
            'categoria_id', 
            'stock', 
            'imagen', 
            'activo',
            'descuento', 
            'destacado', 
            'fecha_creacion', 
            'fecha_actualizacion',
            'vendedor'
        ]
        read_only_fields = [
            'id', 
            'precio_final', 
            'fecha_creacion', 
            'fecha_actualizacion', 
            'vendedor'
        ]
        extra_kwargs = {
            'imagen': {
                'required': False,
                'help_text': _("Imagen principal del producto")
            },
            'activo': {
                'default': True,
                'help_text': _("Indica si el producto está disponible para venta")
            },
            'destacado': {
                'default': False,
                'help_text': _("Indica si el producto aparece como destacado")
            },
            'nombre': {
                'help_text': _("Nombre único del producto. Máx. 255 caracteres")
            },
            'descripcion': {
                'help_text': _("Descripción detallada del producto")
            }
        }

    def get_precio_final(self, obj):
        """Calcula el precio final aplicando el descuento"""
        return obj.precio_final

    def validate(self, data):
        """
        Validaciones adicionales a nivel de objeto:
        - Stock mínimo para productos activos
        - Descuento requerido para productos destacados
        - Coherencia entre precio y descuento
        """
        errors = {}
        
        # Validación de stock mínimo cuando el producto está activo
        if data.get('activo', True) and 'stock' in data and data['stock'] <= 0:
            errors['stock'] = _("No se puede activar un producto sin stock disponible")
            
        # Validación de descuento para productos destacados
        if data.get('destacado', False) and 'descuento' in data and data['descuento'] <= 0:
            errors['descuento'] = _("Los productos destacados deben tener descuento")
            
        # Validación de coherencia precio/descuento
        if 'precio' in data and 'descuento' in data:
            precio_final = data['precio'] * (1 - data['descuento']/100)
            if precio_final <= 0:
                errors['descuento'] = _("El descuento no puede hacer que el precio sea cero o negativo")
        
        if errors:
            raise serializers.ValidationError(errors)
            
        return data

    def validate_nombre(self, value):
        """Validación específica para el nombre del producto"""
        if len(value) < 3:
            raise serializers.ValidationError(
                _("El nombre del producto debe tener al menos 3 caracteres")
            )
        return value

    def create(self, validated_data):
        """
        Crea un nuevo producto asegurando que:
        - Se asigna el vendedor automáticamente
        - Tiene una categoría asociada
        - Se maneja correctamente la imagen
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['vendedor'] = request.user
        
        if 'categoria' not in validated_data:
            raise serializers.ValidationError({
                'categoria_id': _("Este campo es requerido")
            })
            
        imagen = validated_data.pop('imagen', None)
        instance = super().create(validated_data)
        
        if imagen:
            instance.imagen = imagen
            instance.save()
            
        return instance

    def update(self, instance, validated_data):
        """
        Actualiza un producto existente asegurando que:
        - El vendedor no puede ser modificado
        - Se maneja correctamente la imagen
        - Se mantiene la integridad de los datos
        """
        if 'vendedor' in validated_data:
            del validated_data['vendedor']
            
        imagen = validated_data.pop('imagen', None)
        instance = super().update(instance, validated_data)
        
        if imagen:
            instance.imagen = imagen
            instance.save()
            
        return instance

    def to_representation(self, instance):
        """
        Personaliza la representación de los datos:
        - Incluye el precio_final calculado
        - Oculta campos sensibles para no propietarios
        - Formatea los datos para la respuesta
        """
        representation = super().to_representation(instance)
        
        # Asegurar que el precio final esté calculado
        representation['precio_final'] = instance.precio_final
        
        # Ocultar campos sensibles si el usuario no es el vendedor
        request = self.context.get('request')
        if not request or not instance.es_propietario(request.user):
            representation.pop('stock', None)
            representation.pop('vendedor', None)
            
        # Formatear fechas si es necesario
        representation['fecha_creacion'] = instance.fecha_creacion.isoformat()
        representation['fecha_actualizacion'] = instance.fecha_actualizacion.isoformat()
            
        return representation