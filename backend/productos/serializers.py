from rest_framework import serializers
from .models import Producto, Categoria
from django.conf import settings

class CategoriaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    cantidad_productos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'slug',
            'activo', 'imagen', 'imagen_url', 'orden',
            'visible', 'fecha_creacion', 'fecha_actualizacion',
            'cantidad_productos'
        ]
        read_only_fields = ['slug', 'cantidad_productos']
        extra_kwargs = {
            'imagen': {'write_only': True}
        }

    def get_imagen_url(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return self.context['request'].build_absolute_uri(obj.imagen.url)
        return None

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.IntegerField(write_only=True)
    imagen_url = serializers.SerializerMethodField()
    precio_final = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'precio_final',
            'categoria', 'categoria_id', 'stock', 'imagen', 'imagen_url',
            'activo', 'descuento', 'destacado', 'fecha_creacion',
            'fecha_actualizacion'
        ]
        extra_kwargs = {
            'precio': {'min_value': 0.01},
            'stock': {'min_value': 0},
            'descuento': {'min_value': 0, 'max_value': 100},
            'imagen': {'write_only': True}
        }

    def get_imagen_url(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return self.context['request'].build_absolute_uri(obj.imagen.url)
        return None

    def validate_categoria_id(self, value):
        if not Categoria.objects.filter(id=value, activo=True).exists():
            raise serializers.ValidationError("La categoría especificada no existe o está inactiva.")
        return value