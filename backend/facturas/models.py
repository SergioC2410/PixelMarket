from django.db import models
from pedidos.models import Pedido
from django.core.exceptions import ValidationError

class Factura(models.Model):
    """
    Modelo para facturas.
    Ahora permite múltiples facturas por pedido.
    """
    factura_id = models.AutoField(primary_key=True)  # ID numérico secuencial
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='facturas')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_total(self):
        """
        Calcula el total de la factura sumando los productos del pedido.
        Considera la cantidad y el precio unitario de cada ítem.
        """
        if not self.pedido:
            return 0

        # Calcula el total multiplicando cantidad * precio_unitario para cada ítem
        total = self.pedido.items.aggregate(
            total=models.Sum(models.F('cantidad') * models.F('precio_unitario'))
        )['total'] or 0

        return total

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular el total antes de guardar.
        Valida que la factura esté asociada a un pedido y que el pedido tenga ítems.
        """
        if not self.pedido:
            raise ValidationError("Una factura debe estar asociada a un pedido.")

        if not self.pedido.items.exists():
            raise ValidationError("El pedido no tiene ítems para facturar.")

        # Calcula el total antes de guardar
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Representación en cadena de la factura.
        """
        return f"Factura #{self.factura_id} - Pedido #{self.pedido.id} - Total: ${self.total}"