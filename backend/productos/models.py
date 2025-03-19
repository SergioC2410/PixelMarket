# Importamos los módulos necesarios de Django
from django.db import models
from django.utils.text import slugify  # Para generar slugs automáticamente
from django.core.exceptions import ValidationError  # Para validaciones personalizadas

# Definimos el modelo Categoria
class Categoria(models.Model):
    """
    Modelo para representar las categorías de productos.
    Cada categoría tiene un nombre único y una descripción opcional.
    """
    # Campo para el nombre de la categoría (único)
    nombre = models.CharField(max_length=100, unique=True)

    # Campo para la descripción de la categoría (opcional)
    descripcion = models.TextField(blank=True)

    # Campo para el slug (URL amigable)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Método para guardar la categoría.
        Si no se proporciona un slug, se genera automáticamente a partir del nombre.
        """
        if not self.slug:
            self.slug = slugify(self.nombre)  # Genera el slug automáticamente
        super().save(*args, **kwargs)

    def cantidad_productos(self):
        """
        Método para obtener la cantidad de productos asociados a esta categoría.
        """
        return self.productos.count()  # Usa el related_name 'productos'

    def __str__(self):
        """
        Representación en cadena de la categoría (aparece en el panel de administración).
        """
        return self.nombre


# Definimos el modelo Producto
class Producto(models.Model):
    """
    Modelo para representar los productos.
    Cada producto está asociado a una categoría y tiene varios atributos.
    """
    # Campo para el nombre del producto
    nombre = models.CharField(max_length=200)

    # Campo para la descripción del producto (opcional)
    descripcion = models.TextField(blank=True, null=True)

    # Campo para el precio del producto (con 10 dígitos y 2 decimales)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Campo para la categoría del producto (clave foránea)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,  # Si se elimina la categoría, se eliminan sus productos
        related_name='productos'  # Nombre para acceder a los productos desde una categoría
    )

    # Campo para el stock del producto (entero positivo)
    stock = models.PositiveIntegerField(default=0)

    # Campo para la fecha de creación del producto (se asigna automáticamente)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Método para validar los datos del producto antes de guardarlo.
        """
        if self.precio < 0:
            raise ValidationError({'precio': 'El precio no puede ser negativo.'})
        if self.stock < 0:
            raise ValidationError({'stock': 'El stock no puede ser negativo.'})

    def disponible(self):
        """
        Método para verificar si el producto está disponible (stock > 0).
        """
        return self.stock > 0

    def __str__(self):
        """
        Representación en cadena del producto (aparece en el panel de administración).
        """
        return self.nombre