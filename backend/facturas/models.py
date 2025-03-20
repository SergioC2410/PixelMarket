from django.db import models
from pedidos.models import Pedido
from django.core.exceptions import ValidationError

class Factura(models.Model):
    """
    Modelo para facturas.
    Permite múltiples facturas por pedido y calcula automáticamente el total.
    """
    # ID numérico secuencial (no es estrictamente necesario, Django lo hace por defecto)
    factura_id = models.AutoField(primary_key=True)

    # Relación con el pedido (una factura pertenece a un pedido)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='facturas')

    # Fecha de emisión automática (no editable)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    # Total de la factura (calculado automáticamente)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    def calcular_total(self):
        """
        Calcula el total de la factura sumando los productos del pedido.
        Considera la cantidad y el precio unitario de cada ítem.
        """
        if not self.pedido:
            return 0.00

        # Calcula el total multiplicando cantidad * precio_unitario para cada ítem
        total = self.pedido.items.aggregate(
            total=models.Sum(models.F('cantidad') * models.F('precio_unitario'))
        )['total'] or 0.00

        return total

    def clean(self):
        """
        Valida la factura antes de guardarla.
        - Asegura que la factura esté asociada a un pedido.
        - Verifica que el pedido tenga ítems.
        """
        if not self.pedido:
            raise ValidationError("Una factura debe estar asociada a un pedido.")

        if not self.pedido.items.exists():
            raise ValidationError("El pedido no tiene ítems para facturar.")

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular el total antes de guardar.
        """
        # Valida el modelo antes de guardar
        self.clean()

        # Calcula el total antes de guardar
        self.total = self.calcular_total()

        # Guarda la factura
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Representación en cadena de la factura.
        """
        return f"Factura #{self.factura_id} - Pedido #{self.pedido.id} - Total: ${self.total:.2f}"