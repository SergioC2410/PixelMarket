from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from pedidos.models import Pedido
from django.core.exceptions import ValidationError

class Factura(models.Model):
    """
    Modelo Factura corregido sin null=True en el campo id
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name='factura',
        verbose_name='Pedido asociado'
    )
    
    fecha_emision = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de emisión'
    )
    
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Total'
    )
    
    numero_factura = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='Número de factura'
    )
    
    archivo_pdf = models.FileField(
        upload_to='facturas/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Archivo PDF'
    )

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"{self.numero_factura} - ${self.total}"

    def save(self, *args, **kwargs):
        """Genera número de factura si no existe"""
        if not self.numero_factura:
            anio_mes = timezone.now().strftime('%Y%m')
            ultima = Factura.objects.filter(
                numero_factura__startswith=f'FAC-{anio_mes}'
            ).order_by('-numero_factura').first()
            consecutivo = (int(ultima.numero_factura[-4:]) + 1 if ultima else 1)
            self.numero_factura = f"FAC-{anio_mes}-{consecutivo:04d}"
        
        if not self.total and hasattr(self.pedido, 'items'):
            self.total = sum(
                item.cantidad * item.precio_unitario 
                for item in self.pedido.items.all()
            )
            
        super().save(*args, **kwargs)