# Este archivo es opcional, pero muy útil si usas Django REST Framework (DRF) para crear APIs.
from rest_framework import serializers
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Categoria.
    Convierte objetos Categoria en JSON y viceversa.
    """
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Producto.
    Convierte objetos Producto en JSON y viceversa.
    """
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'stock', 'fecha_creacion']

    def create(self, validated_data):
        """
        Crea un nuevo producto con los datos validados.
        """
        categoria_id = self.context.get('categoria_id')
        categoria = Categoria.objects.get(id=categoria_id)
        producto = Producto.objects.create(categoria=categoria, **validated_data)
        return producto

# Mejoras sugeridas:
# 1. Agregar validaciones personalizadas (ej: precio mínimo).
# 2. Implementar serializadores para actualización parcial (PATCH).
