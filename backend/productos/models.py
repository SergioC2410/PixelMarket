# Importamos los módulos necesarios de Django
from django.db import models
from django.utils.text import slugify  # Para generar slugs automáticamente
from django.core.exceptions import ValidationError  # Para validaciones personalizadas
from django.core.validators import MinValueValidator  # Para validaciones de valores negativos

# Definimos el modelo Categoria para representar las categorías de productos
class Categoria(models.Model):
    """
    Modelo para representar las categorías de productos.
    Cada categoría tiene un nombre único y una descripción opcional.
    """
    # Campo para el nombre de la categoría (único)
    nombre = models.CharField(max_length=100, unique=True)

    # Campo para la descripción de la categoría (opcional)
    descripcion = models.TextField(blank=True)

    # Campo para el slug (URL amigable) de la categoría
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Método para guardar la categoría.
        Si no se proporciona un slug, se genera automáticamente a partir del nombre.
        """
        if not self.slug:
            self.slug = slugify(self.nombre)  # Genera el slug automáticamente si no se proporciona
        super().save(*args, **kwargs)

    def cantidad_productos(self):
        """
        Método para obtener la cantidad de productos asociados a esta categoría.
        Utiliza el related_name 'productos' para acceder a los productos desde la categoría.
        """
        return self.productos.count()

    def __str__(self):
        """
        Representación en cadena de la categoría.
        Aparece como el nombre de la categoría en el panel de administración de Django.
        """
        return str(self.nombre)


# Definimos el modelo Producto para representar los productos en la tienda
class Producto(models.Model):
    """
    Modelo para representar los productos.
    Cada producto está asociado a una categoría y tiene varios atributos como precio, stock y fecha de creación.
    """
    # Campo para el nombre del producto
    nombre = models.CharField(max_length=255, unique=True)

    # Campo para la descripción del producto (opcional)
    descripcion = models.TextField()

    # Campo para el precio del producto (con validación para que no sea negativo)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    # Campo para la categoría del producto (clave foránea)
    categoria = models.ForeignKey(
        Categoria,  # Relacionamos el producto con una categoría
        on_delete=models.CASCADE,  # Si se elimina la categoría, se eliminan sus productos
        related_name='productos'  # Permite acceder a los productos desde una categoría
    )

    # Campo para el stock del producto (entero positivo)
    stock = models.PositiveIntegerField(default=0)

    # Campo para la fecha de creación del producto (se asigna automáticamente)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Campo para la imagen del producto
    # Este campo permite subir una imagen del producto, y se guarda en la carpeta 'productos/' dentro del directorio de medios.
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def clean(self):
        """
        Método de validación personalizado que se ejecuta antes de guardar el producto.
        Verifica que el precio y el stock no sean negativos.
        """
        if self.precio < 0:
            raise ValidationError({'precio': 'El precio no puede ser negativo.'})
        if self.stock < 0:
            raise ValidationError({'stock': 'El stock no puede ser negativo.'})

    def disponible(self):
        """
        Método que verifica si el producto está disponible (stock > 0).
        Retorna True si el stock es mayor que cero, de lo contrario False.
        """
        return self.stock > 0

    def __str__(self):
        """
        Representación en cadena del producto.
        Aparece como el nombre del producto en el panel de administración de Django.
        """
        return str(self.nombre)
