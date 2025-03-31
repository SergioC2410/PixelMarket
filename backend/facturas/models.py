from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from pedidos.models import Pedido
import os

class Factura(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name='factura'
    )
    fecha_emision = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    numero_factura = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    archivo_pdf = models.FileField(
        upload_to='facturas/%Y/%m/%d',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            self.numero_factura = f"FAC-{timezone.now().strftime('%Y%m')}-{Factura.objects.count() + 1:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_factura} - ${self.total}"