from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from usuarios.models import Usuario  # Importación del modelo Usuario

class Categoria(models.Model):
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
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    visible = models.BooleanField(
        default=True,
        verbose_name="Visible en frontend"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['orden', 'nombre']
        indexes = [
            models.Index(fields=['nombre'], name='categoria_nombre_idx'),
            models.Index(fields=['activo'], name='categoria_activo_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    vendedor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='productos_vendidos',
        verbose_name="Vendedor",
        null=True,  # Temporalmente nullable para migración existente
        blank=True  # Temporalmente en blanco para migración existente
    )
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
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Porcentaje de descuento"
    )
    destacado = models.BooleanField(default=False, verbose_name="Producto destacado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre'], name='producto_nombre_idx'),
            models.Index(fields=['categoria'], name='producto_categoria_idx'),
            models.Index(fields=['activo'], name='producto_activo_idx'),
            models.Index(fields=['destacado'], name='producto_destacado_idx'),
            models.Index(fields=['vendedor'], name='producto_vendedor_idx'),
        ]

    @property
    def precio_final(self):
        """Calcula el precio final aplicando el descuento"""
        return round(self.precio * (1 - self.descuento/100), 2)

    def clean(self):
        """Validaciones adicionales del modelo"""
        super().clean()
        
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo")
            
        if self.precio <= 0:
            raise ValidationError("El precio debe ser mayor que cero")

    def save(self, *args, **kwargs):
        """Guarda el producto asignando automáticamente el vendedor si es nuevo"""
        if not self.pk and not self.vendedor and hasattr(kwargs.get('request'), 'user'):
            self.vendedor = kwargs['request'].user
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL para acceder al detalle del producto"""
        return reverse('producto-detail', kwargs={'pk': self.pk})

    def reducir_stock(self, cantidad):
        """Reduce el stock del producto"""
        if cantidad > self.stock:
            raise ValidationError("No hay suficiente stock disponible")
        self.stock -= cantidad
        self.save()

    def aumentar_stock(self, cantidad):
        """Aumenta el stock del producto"""
        self.stock += cantidad
        self.save()

    def es_propietario(self, user):
        """Verifica si el usuario es propietario del producto"""
        return self.vendedor == user

    def __str__(self):
        """Representación en cadena del producto"""
        vendedor_info = f" - Vendedor: {self.vendedor.email}" if self.vendedor else ""
        return f"{self.nombre} (${self.precio_final}){vendedor_info}"