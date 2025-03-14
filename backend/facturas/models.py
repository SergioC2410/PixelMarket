# Este archivo define el modelo de la base de datos para las facturas.
from django.db import models
from pedidos.models import Pedido  # Importa el modelo Pedido

class Factura(models.Model):
    """
    Modelo para facturas.
    Una factura está asociada a un pedido.
    """
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='factura')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        Representación en cadena de la factura (aparece en el panel de administración).
        """
        return f"Factura #{self.id} - Pedido #{self.pedido.id}"

    # Mejoras sugeridas:
    # 1. Agregar un método para calcular el total automáticamente.
    # 2. Implementar validaciones (ej: no permitir facturas sin pedido).