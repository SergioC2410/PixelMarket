from rest_framework import serializers
from .models import Producto, Categoria, ImagenProducto
from django.conf import settings

class CategoriaSerializer(serializers.ModelSerializer):
    cantidad_productos = serializers.IntegerField(read_only=True)
    imagen_url = serializers.SerializerMethodField()
    icono_url = serializers.SerializerMethodField()  


    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'slug', 
            'activo', 'imagen', 'imagen_url', 'cantidad_productos',
            'icono', 'icono_url', 'orden', 'visible',  # Campos agregados
            'fecha_creacion', 'fecha_actualizacion'    # Campos adicionales de BD
        ]
        read_only_fields = ['slug', 'cantidad_productos']
        extra_kwargs = {
            'imagen': {'write_only': True},
            'icono': {'write_only': True}  # Si el campo se escribe directamente
        }


    def get_icono_url(self, obj):
        if not obj.icono:
            return None
        
        # Verificar si el request está en el contexto
        if 'request' in self.context:
            return self.context['request'].build_absolute_uri(settings.STATIC_URL + obj.icono)
        else:
            # Usar STATIC_URL directamente si no hay request
            return f"{settings.STATIC_URL}{obj.icono}"


    def get_imagen_url(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return self.context['request'].build_absolute_uri(obj.imagen.url)
        return None


    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

class ImagenProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'imagen_url', 'orden']
        read_only_fields = ['id']

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
    imagenes_adicionales = ImagenProductoSerializer(
        many=True, 
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'precio_final',
            'categoria', 'categoria_id', 'stock', 'fecha_creacion',
            'fecha_actualizacion', 'imagen', 'imagen_url', 'activo',
            'descuento', 'destacado', 'imagenes_adicionales'
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

    def create(self, validated_data):
        # Manejo de creación con imágenes adicionales
        imagenes_data = self.context['request'].FILES.getlist('imagenes_adicionales')
        categoria_id = validated_data.pop('categoria_id')
        producto = Producto.objects.create(
            categoria_id=categoria_id,
            **validated_data
        )
        
        for i, imagen_data in enumerate(imagenes_data):
            ImagenProducto.objects.create(
                producto=producto,
                imagen=imagen_data,
                orden=i
            )
        
        return producto

    def update(self, instance, validated_data):
        # Manejo de actualización con imágenes
        imagenes_data = self.context['request'].FILES.getlist('imagenes_adicionales')
        categoria_id = validated_data.pop('categoria_id', None)
        
        if categoria_id:
            instance.categoria_id = categoria_id
        
        instance = super().update(instance, validated_data)
        
        if imagenes_data:
            # Eliminar imágenes existentes si se envían nuevas
            instance.imagenes_adicionales.all().delete()
            for i, imagen_data in enumerate(imagenes_data):
                ImagenProducto.objects.create(
                    producto=instance,
                    imagen=imagen_data,
                    orden=i
                )
        
        return instance