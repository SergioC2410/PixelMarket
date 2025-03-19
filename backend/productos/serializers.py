# Importamos los módulos necesarios de Django REST Framework (DRF)
from rest_framework import serializers

# Importamos los modelos que vamos a serializar
from .models import Producto, Categoria

# Definimos el serializador para el modelo Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Categoria.
    Convierte objetos Categoria en JSON y viceversa.
    """
    class Meta:
        # Especificamos el modelo que se va a serializar
        model = Categoria
        # Especificamos los campos que se incluirán en la serialización
        fields = ['id', 'nombre', 'descripcion', 'slug']

    def validate_nombre(self, value):
        """
        Validación personalizada para el campo 'nombre'.
        Asegura que el nombre no esté vacío.
        """
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value


# Definimos el serializador para el modelo Producto
class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Producto.
    Convierte objetos Producto en JSON y viceversa.
    """
    # Incluimos el serializador de Categoria para mostrar detalles de la categoría
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        # Especificamos el modelo que se va a serializar
        model = Producto
        # Especificamos los campos que se incluirán en la serialización
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'stock', 'fecha_creacion']

    def validate_precio(self, value):
        """
        Validación personalizada para el campo 'precio'.
        Asegura que el precio no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_stock(self, value):
        """
        Validación personalizada para el campo 'stock'.
        Asegura que el stock no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def create(self, validated_data):
        """
        Método para crear un nuevo producto.
        Obtiene el ID de la categoría del contexto y asocia el producto a la categoría.
        """
        categoria_id = self.context.get('categoria_id')
        categoria = Categoria.objects.get(id=categoria_id)
        producto = Producto.objects.create(categoria=categoria, **validated_data)
        return producto


# Definimos un serializador para actualización parcial de productos (PATCH)
class ProductoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualización parcial del modelo Producto.
    Permite actualizar solo algunos campos del producto.
    """
    class Meta:
        # Especificamos el modelo que se va a serializar
        model = Producto
        # Especificamos los campos que se pueden actualizar
        fields = ['nombre', 'descripcion', 'precio', 'stock']

    def validate_precio(self, value):
        """
        Validación personalizada para el campo 'precio'.
        Asegura que el precio no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_stock(self, value):
        """
        Validación personalizada para el campo 'stock'.
        Asegura que el stock no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value