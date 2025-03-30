from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from pedidos.models import Pedido
import os
from datetime import datetime

class Factura(models.Model):
    """
    Modelo mejorado para facturas con:
    - Relación con Pedidos y Usuarios
    - Generación automática de números de factura
    - Almacenamiento de PDF
    - Validaciones integradas
    """
    
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,  # Modificado para mayor seguridad
        related_name='factura',
        verbose_name='Pedido asociado',
        help_text='Pedido al que pertenece esta factura'
    )
    
    fecha_emision = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de emisión',
        help_text='Fecha y hora cuando se generó la factura'
    )
    
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Total facturado',
        help_text='Monto total en moneda local'
    )
    
    numero_factura = models.CharField(
        max_length=20,
        unique=True,
        editable=False,  # No editable manualmente
        verbose_name='Número de factura',
        help_text='Número único generado automáticamente'
    )
    
    archivo_pdf = models.FileField(
        upload_to='facturas/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Archivo PDF',
        help_text='PDF generado automáticamente'
    )

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
        indexes = [
            models.Index(fields=['numero_factura']),
            models.Index(fields=['pedido']),
        ]
        permissions = [
            ('generar_factura', 'Puede generar facturas'),
            ('descargar_factura', 'Puede descargar facturas'),
        ]

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.pedido.usuario.nombre_completo()} (${self.total})"

    def save(self, *args, **kwargs):
        """Genera automáticamente el número de factura al crear"""
        if not self.numero_factura:
            fecha_codigo = datetime.now().strftime('%Y%m')
            ultima_factura = Factura.objects.order_by('-id').first()
            consecutivo = (ultima_factura.id + 1) if ultima_factura else 1
            self.numero_factura = f"FAC-{fecha_codigo}-{consecutivo:04d}"
        
        if not self.total and hasattr(self.pedido, 'total'):
            self.total = self.pedido.total
            
        super().save(*args, **kwargs)

    def generar_nombre_pdf(self):
        """Genera nombre descriptivo para el archivo PDF"""
        return f"factura_{self.numero_factura}_{self.fecha_emision.strftime('%Y%m%d')}.pdf"

    def calcular_total(self):
        """Calcula el total basado en los ítems del pedido"""
        if hasattr(self.pedido, 'items'):
            self.total = sum(
                item.cantidad * item.precio_unitario 
                for item in self.pedido.items.all()
            )
        return self.total

    @property
    def datos_cliente(self):
        """Diccionario con datos estructurados del cliente"""
        return {
            'nombre': self.pedido.usuario.nombre_completo(),
            'cedula': self.pedido.usuario.cedula,
            'direccion': self.pedido.usuario.direccion,
            'telefono': str(self.pedido.usuario.telefono),
            'email': self.pedido.usuario.email
        }