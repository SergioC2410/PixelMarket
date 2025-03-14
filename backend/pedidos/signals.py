# Este archivo contiene la lógica para actualizar el inventario cuando se crea un pedido.

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ItemPedido
from productos.models import Producto

@receiver(post_save, sender=ItemPedido)
def actualizar_inventario(sender, instance, **kwargs):
    """
    Señal para actualizar el inventario cuando se crea un ítem de pedido.
    """
    producto = instance.producto
    producto.stock -= instance.cantidad
    producto.save()

    # Mejoras sugeridas:
    # 1. Agregar validaciones para evitar stock negativo.
    # 2. Implementar notificaciones si el stock es bajo.
