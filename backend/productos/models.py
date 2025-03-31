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
    activo = models.BooleanField(default=True, verbose_name="Activo")
    imagen = models.ImageField(
        upload_to='categorias/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Imagen de categoría"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'], name='categoria_nombre_idx'),
            models.Index(fields=['activo'], name='categoria_activo_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def cantidad_productos(self):
        return self.productos.filter(activo=True).count()

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
        validators=[MinValueValidator(0.01)],
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
        verbose_name="Imagen principal"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Porcentaje de descuento"
    )
    destacado = models.BooleanField(default=False, verbose_name="Producto destacado")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre'], name='producto_nombre_idx'),
            models.Index(fields=['categoria'], name='producto_categoria_idx'),
            models.Index(fields=['activo'], name='producto_activo_idx'),
            models.Index(fields=['destacado'], name='producto_destacado_idx'),
            models.Index(fields=['precio'], name='producto_precio_idx'),
        ]

    def clean(self):
        """Validaciones adicionales"""
        if self.stock < 0:
            raise ValidationError({'stock': 'El stock no puede ser negativo.'})
        if self.descuento < 0 or self.descuento > 100:
            raise ValidationError({'descuento': 'El descuento debe estar entre 0 y 100.'})

    @property
    def precio_final(self):
        """Calcula el precio con descuento aplicado"""
        return round(self.precio * (1 - self.descuento/100), 2)

    @property
    def disponible(self):
        """Indica si el producto está disponible para venta"""
        return self.stock > 0 and self.activo

    @property
    def imagen_url(self):
        """Devuelve la URL completa de la imagen"""
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        return None

    def get_absolute_url(self):
        return reverse('producto-detail', kwargs={'pk': self.pk})

    def soft_delete(self):
        """Eliminación lógica del producto"""
        self.activo = False
        self.save()

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

class ImagenProducto(models.Model):
    """
    Modelo para imágenes adicionales de productos (galería)
    """
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes_adicionales'
    )
    imagen = models.ImageField(
        upload_to='productos/galeria/%Y/%m/%d/',
        verbose_name="Imagen adicional"
    )
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ['orden', 'fecha_creacion']
        unique_together = ['producto', 'orden']

    def __str__(self):
        return f"Imagen #{self.orden} de {self.producto.nombre}"