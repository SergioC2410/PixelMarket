from rest_framework import serializers
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'slug']
        read_only_fields = ['slug']  # Si slug es autogenerado

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)  # Para respuesta detallada
    categoria_id = serializers.IntegerField(write_only=True)  # Para recibir ID en creación/actualización
    imagen_url = serializers.ImageField(source='imagen', read_only=True)  # URL completa automática

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 
            'categoria', 'categoria_id', 'stock', 
            'fecha_creacion', 'imagen', 'imagen_url'
        ]
        extra_kwargs = {
            'precio': {'min_value': 0},
            'stock': {'min_value': 0}
        }

    def validate_categoria_id(self, value):
        if not Categoria.objects.filter(id=value).exists():
            raise serializers.ValidationError("La categoría especificada no existe.")
        return value

    def create(self, validated_data):
        # Asignación segura de categoría via categoria_id
        categoria_id = validated_data.pop('categoria_id')
        categoria = Categoria.objects.get(id=categoria_id)
        return Producto.objects.create(categoria=categoria, **validated_data)

    def update(self, instance, validated_data):
        # Actualización de categoría si se envía categoria_id
        categoria_id = validated_data.pop('categoria_id', None)
        if categoria_id:
            instance.categoria = Categoria.objects.get(id=categoria_id)
        return super().update(instance, validated_data)