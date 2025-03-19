# Este archivo define los modelos de la base de datos para pedidos y ítems de pedido.

from django.db import models
from django.core.exceptions import ValidationError
from productos.models import Producto  # Importa el modelo Producto
from usuarios.models import Usuario    # Importa el modelo Usuario

class Pedido(models.Model):
    """
    Modelo para pedidos.
    Un pedido está asociado a un usuario (comprador) y tiene varios ítems.
    """
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        """
        Representación en cadena del pedido (aparece en el panel de administración).
        """
        return f"Pedido #{self.id} - {self.usuario.username}"

    def calcular_total(self):
        """
        Calcula el total del pedido sumando el subtotal de todos los ítems.
        """
        self.total = sum(item.subtotal() for item in self.items.all())
        self.save()

    def clean(self):
        """
        Valida que el pedido tenga al menos un ítem antes de guardarlo.
        """
        if self.items.count() == 0:
            raise ValidationError("Un pedido no puede estar vacío.")

    class Meta:
        """
        Metadata del modelo Pedido.
        """
        ordering = ['-fecha_creacion']  # Ordenar pedidos por fecha de creación descendente
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class ItemPedido(models.Model):
    """
    Modelo para ítems de pedido.
    Un ítem está asociado a un pedido y a un producto.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        Representación en cadena del ítem (aparece en el panel de administración).
        """
        return f"{self.cantidad}x {self.producto.nombre}"

    def subtotal(self):
        """
        Calcula el subtotal del ítem (cantidad * precio_unitario).
        """
        return self.cantidad * self.precio_unitario

    def clean(self):
        """
        Valida que la cantidad no sea negativa y que no exceda el stock disponible.
        """
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")
        if self.cantidad > self.producto.stock:
            raise ValidationError(f"No hay suficiente stock para {self.producto.nombre}. Stock disponible: {self.producto.stock}")

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para actualizar el total del pedido después de guardar el ítem.
        """
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

    class Meta:
        """
        Metadata del modelo ItemPedido.
        """
        verbose_name = 'Ítem de Pedido'
        verbose_name_plural = 'Ítems de Pedido'