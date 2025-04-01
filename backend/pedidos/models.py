from django.db import models
from django.core.exceptions import ValidationError
from productos.models import Producto
from usuarios.models import Usuario
from django.utils.translation import gettext_lazy as _
from usuarios.models import Ubicacion 
class Pedido(models.Model):
    """
    Modelo para pedidos con integración completa de usuarios.
    Un pedido está asociado a un usuario (comprador) y contiene múltiples ítems.
    """
    ubicacion_entrega = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Ubicación de entrega"
    )
    class EstadoPedido(models.TextChoices):
        PENDIENTE_PAGO = 'pendiente_pago', _('Pendiente de Pago')
        PAGADO = 'pagado', _('Pagado')
        EN_PROCESO = 'en_proceso', _('En Proceso')
        ENVIADO = 'enviado', _('Enviado')
        COMPLETADO = 'completado', _('Completado')
        CANCELADO = 'cancelado', _('Cancelado')
        REEMBOLSADO = 'reembolsado', _('Reembolsado')

    class MetodoEntrega(models.TextChoices):
        DOMICILIO = 'domicilio', _('A domicilio')
        RETIRAR = 'retirar', _('Retirar en tienda')
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name=_('Comprador')
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última actualización')
    )
    estado = models.CharField(
        max_length=15,
        choices=EstadoPedido.choices,
        default=EstadoPedido.PENDIENTE_PAGO,
        verbose_name=_('Estado')
    )
    metodo_entrega = models.CharField(
        max_length=10,
        choices=MetodoEntrega.choices,
        default=MetodoEntrega.DOMICILIO,
        verbose_name=_('Método de entrega')
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Total del pedido')
    )
    direccion_entrega = models.TextField(
        blank=True,
        verbose_name=_('Dirección de entrega')
    )
    metodo_pago = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Método de pago')
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = _('Pedido')
        verbose_name_plural = _('Pedidos')
        indexes = [
            models.Index(fields=['usuario'], name='pedido_usuario_idx'),
            models.Index(fields=['estado'], name='pedido_estado_idx'),
            models.Index(fields=['fecha_creacion'], name='pedido_fecha_idx'),
        ]

    def __str__(self):
        return _('Pedido #%(id)s - %(usuario)s (%(estado)s)') % {
            'id': self.id,
            'usuario': self.usuario.email,
            'estado': self.get_estado_display()
        }

    def calcular_total(self):
        """Calcula el total sumando todos los ítems del pedido"""
        self.total = sum(item.subtotal() for item in self.items.all())
        self.save(update_fields=['total', 'fecha_actualizacion'])

    def actualizar_stock(self, accion='restar'):
        """
        Actualiza el stock de los productos según el estado del pedido
        accion: 'restar' (al confirmar) o 'sumar' (al cancelar)
        """
        for item in self.items.all():
            if accion == 'restar':
                item.producto.reducir_stock(item.cantidad)
            elif accion == 'sumar':
                item.producto.aumentar_stock(item.cantidad)

    def clean(self):
        """Validaciones complejas del modelo"""
        errors = {}
        
        if self.items.count() == 0:
            errors['items'] = _('El pedido debe contener al menos un ítem.')
            
        if (self.metodo_entrega == self.MetodoEntrega.DOMICILIO and 
            not self.direccion_entrega):
            errors['direccion_entrega'] = _('Se requiere dirección para envío a domicilio.')
        
        if errors:
            raise ValidationError(errors)

class ItemPedido(models.Model):
    """
    Modelo para ítems de pedido con validación de stock.
    Relaciona productos con pedidos y almacena cantidades.
    """
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Pedido asociado')
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        verbose_name=_('Producto')
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Cantidad')
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Precio unitario')
    )

    class Meta:
        verbose_name = _('Ítem de pedido')
        verbose_name_plural = _('Ítems de pedido')
        constraints = [
            models.UniqueConstraint(
                fields=['pedido', 'producto'],
                name='unique_producto_en_pedido'
            )
        ]

    def __str__(self):
        return f"{self.cantidad} × {self.producto.nombre}"

    def subtotal(self):
        """Calcula el subtotal del ítem"""
        return self.cantidad * self.precio_unitario

    def clean(self):
        """Validaciones de cantidad y stock"""
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': _('La cantidad debe ser mayor que cero.')})
        
        if hasattr(self, 'producto') and self.cantidad > self.producto.stock:
            raise ValidationError({
                'cantidad': _('Stock insuficiente. Disponible: %(stock)s') % {
                    'stock': self.producto.stock
                }
            })

    def save(self, *args, **kwargs):
        """
        Guarda el ítem y actualiza:
        1. El precio unitario al momento de creación
        2. El total del pedido
        """
        if not self.pk:  # Solo en creación
            self.precio_unitario = self.producto.precio_final
            
        super().save(*args, **kwargs)
        self.pedido.calcular_total()