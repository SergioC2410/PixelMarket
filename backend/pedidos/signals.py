# Este archivo contiene la lógica para actualizar el inventario cuando se crea un ítem de pedido.

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import ItemPedido
from productos.models import Producto

@receiver(post_save, sender=ItemPedido)
def actualizar_inventario(sender, instance, **kwargs):
    """
    Señal para actualizar el inventario cuando se crea o modifica un ítem de pedido.
    Se asegura de que el stock no sea negativo.
    """
    producto = instance.producto

    # Validar que la cantidad no sea mayor que el stock disponible
    if instance.cantidad > producto.stock:
        raise ValidationError(
            f"No hay suficiente stock para el producto {producto.nombre}. "
            f"Stock disponible: {producto.stock}, Cantidad solicitada: {instance.cantidad}"
        )

    # Actualizar el stock del producto
    producto.stock -= instance.cantidad
    producto.save()

    # Opcional: Imprimir un mensaje en la consola para depuración
    print(f"Stock actualizado para {producto.nombre}. Nuevo stock: {producto.stock}")