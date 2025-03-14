# Este archivo define los modelos de la base de datos para productos y categorías.
from django.db import models

class Categoria(models.Model):
    """
    Modelo para categorías de productos.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Representación en cadena de la categoría (aparece en el panel de administración).
        """
        return self.nombre

    # Mejoras sugeridas:
    # 1. Agregar un campo `slug` para URLs amigables.
    # 2. Implementar métodos útiles, como `cantidad_productos()`.

class Producto(models.Model):
    """
    Modelo para productos.
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    stock = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Representación en cadena del producto (aparece en el panel de administración).
        """
        return self.nombre

    # Mejoras sugeridas:
    # 1. Agregar validaciones personalizadas (ej: precio mínimo).
    # 2. Implementar métodos útiles, como `disponible()` para verificar el stock.