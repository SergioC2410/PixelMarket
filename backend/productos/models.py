from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

class Categoria(models.Model):
    """
    Modelo para categorías de productos con slug automático y relación inversa a productos.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    slug = models.SlugField(unique=True, blank=True, max_length=110)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def cantidad_productos(self):
        return self.productos.count()

    def get_absolute_url(self):
        return reverse('categoria-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    """
    Modelo principal para productos con validaciones integradas y manejo de imágenes.
    """
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre del producto")
    descripcion = models.TextField(blank=True, default='Sin descripción', verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],  # Precio mínimo de 0.01
        verbose_name="Precio unitario"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name="Categoría asociada"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Unidades disponibles")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    imagen = models.ImageField(
        upload_to='productos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Imagen del producto"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre'], name='producto_nombre_idx'),
            models.Index(fields=['categoria'], name='producto_categoria_idx'),
        ]

    def clean(self):
        """Validación adicional para stock negativo (aunque PositiveIntegerField lo previene)"""
        if self.stock < 0:
            raise ValidationError({'stock': 'El stock no puede ser negativo.'})

    @property
    def disponible(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse('producto-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.nombre} (${self.precio})"