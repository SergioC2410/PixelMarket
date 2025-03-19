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
        model = Categoria  # Especificamos el modelo que vamos a serializar
        fields = ['id', 'nombre', 'descripcion', 'slug']  # Campos que se incluirán en la serialización

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
    categoria = CategoriaSerializer(read_only=True)  # Solo lectura, no se permite modificar la categoría directamente
    imagen_url = serializers.SerializerMethodField()  # Para obtener la URL de la imagen (aunque no se almacena en el modelo como tal)

    class Meta:
        model = Producto  # Especificamos el modelo que vamos a serializar
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'stock', 'fecha_creacion', 'imagen', 'imagen_url']  # Campos a serializar

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
        categoria_id = self.context.get('categoria_id')  # Recuperamos el ID de la categoría desde el contexto
        categoria = Categoria.objects.get(id=categoria_id)  # Obtenemos la categoría de la base de datos
        producto = Producto.objects.create(categoria=categoria, **validated_data)  # Creamos el producto con la categoría asociada
        return producto

    def get_imagen_url(self, obj):
        """
        Método para obtener la URL de la imagen de un producto.
        Retorna la URL completa de la imagen, si existe.
        """
        if obj.imagen:
            # Si el producto tiene una imagen, devolvemos la URL completa de la imagen
            return obj.imagen.url
        return None  # Si no tiene imagen, devolvemos None

# Definimos un serializador para actualización parcial de productos (PATCH)
class ProductoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualización parcial del modelo Producto.
    Permite actualizar solo algunos campos del producto.
    """
    class Meta:
        model = Producto  # Especificamos el modelo que se va a serializar
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']  # Campos que se pueden actualizar

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
