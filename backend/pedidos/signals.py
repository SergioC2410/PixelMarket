from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import ItemPedido, Pedido
from productos.models import Producto
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=ItemPedido)
def validar_stock_antes_de_guardar(sender, instance, **kwargs):
    """
    Valida el stock disponible antes de guardar un ítem de pedido.
    """
    if not instance.pk:  # Solo para nuevos ítems
        producto = instance.producto
        if instance.cantidad > producto.stock:
            raise ValidationError(
                f"Stock insuficiente para {producto.nombre}. "
                f"Disponible: {producto.stock}, Solicitado: {instance.cantidad}"
            )

@receiver(post_save, sender=ItemPedido)
def actualizar_inventario(sender, instance, created, **kwargs):
    """
    Actualiza el inventario cuando se crea o modifica un ítem de pedido.
    Maneja transacciones atómicas para consistencia de datos.
    """
    with transaction.atomic():
        producto = Producto.objects.select_for_update().get(pk=instance.producto.id)
        
        if created:
            producto.stock -= instance.cantidad
            logger.info(
                f"Stock reducido para {producto.nombre}. "
                f"Cantidad: {instance.cantidad}, Nuevo stock: {producto.stock}"
            )
        else:
            # Manejar actualizaciones de cantidad
            old_item = ItemPedido.objects.get(pk=instance.pk)
            diff = old_item.cantidad - instance.cantidad
            producto.stock += diff  # Si la nueva cantidad es menor, se suma la diferencia
            
            logger.info(
                f"Stock ajustado para {producto.nombre}. "
                f"Diferencia: {diff}, Nuevo stock: {producto.stock}"
            )
        
        producto.save()

@receiver(post_delete, sender=ItemPedido)
def restaurar_stock_al_eliminar(sender, instance, **kwargs):
    """
    Restaura el stock cuando se elimina un ítem de pedido.
    """
    with transaction.atomic():
        producto = Producto.objects.select_for_update().get(pk=instance.producto.id)
        producto.stock += instance.cantidad
        producto.save()
        logger.info(
            f"Stock restaurado para {producto.nombre}. "
            f"Cantidad: {instance.cantidad}, Nuevo stock: {producto.stock}"
        )

@receiver(post_save, sender=Pedido)
def manejar_cambios_estado_pedido(sender, instance, **kwargs):
    """
    Maneja actualizaciones de stock cuando cambia el estado del pedido.
    """
    if 'estado' in kwargs.get('update_fields', []) or kwargs.get('created'):
        with transaction.atomic():
            if instance.estado == Pedido.EstadoPedido.CANCELADO:
                for item in instance.items.all():
                    item.producto.stock += item.cantidad
                    item.producto.save()
                logger.info(f"Stock restaurado por cancelación del pedido {instance.id}")
            
            elif instance.estado == Pedido.EstadoPedido.PAGADO and 'estado' in kwargs.get('update_fields', []):
                logger.info(f"Pedido {instance.id} marcado como pagado - stock confirmado")