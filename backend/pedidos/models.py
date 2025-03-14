# Este archivo define los modelos de la base de datos para pedidos y ítems de pedido.

from django.db import models
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

    # Mejoras sugeridas:
    # 1. Agregar un método para calcular el total automáticamente.
    # 2. Implementar validaciones (ej: no permitir pedidos vacíos).

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

    # Mejoras sugeridas:
    # 1. Agregar un método para calcular el subtotal (cantidad * precio_unitario).
    # 2. Implementar validaciones (ej: no permitir cantidades negativas).