from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from pedidos.models import Pedido
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Factura(models.Model):
    """
    Modelo Factura con todas las validaciones y mejoras solicitadas
    """
    class EstadoFactura(models.TextChoices):
        PAGADA = 'P', _('Pagada')
        PENDIENTE = 'N', _('Pendiente')
        ANULADA = 'A', _('Anulada')

    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name='factura',
        verbose_name='Pedido asociado',
        help_text=_('Pedido al que pertenece esta factura')
    )
    
    fecha_emision = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de emisión',
        help_text=_('Fecha y hora cuando se generó la factura')
    )
    
    fecha_vencimiento = models.DateField(
        verbose_name='Fecha de vencimiento',
        null=True,
        blank=True,
        help_text=_('Fecha límite de pago de la factura')
    )
    
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Total',
        help_text=_('Total a pagar en la factura')
    )
    
    iva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='IVA',
        help_text=_('Valor del IVA calculado')
    )
    
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Subtotal',
        help_text=_('Valor antes de aplicar impuestos')
    )
    
    numero_factura = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='Número de factura',
        help_text=_('Número único de identificación de la factura')
    )
    
    estado = models.CharField(
        max_length=1,
        choices=EstadoFactura.choices,
        default=EstadoFactura.PENDIENTE,
        verbose_name='Estado',
        help_text=_('Estado actual de la factura')
    )
    
    metodo_pago = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Método de pago',
        help_text=_('Forma en que se realizó el pago')
    )
    
    archivo_pdf = models.FileField(
        upload_to='facturas/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Archivo PDF',
        help_text=_('Documento PDF generado para la factura')
    )
    
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='facturas_creadas',
        verbose_name='Creado por',
        null=True,
        help_text=_('Usuario que generó la factura')
    )
    
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name='Observaciones',
        help_text=_('Notas adicionales sobre la factura')
    )

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
        permissions = [
            ('view_all_facturas', _('Puede ver todas las facturas')),
            ('change_estado_factura', _('Puede cambiar el estado de factura')),
            ('anular_factura', _('Puede anular facturas')),
        ]
        indexes = [
            models.Index(fields=['numero_factura']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_emision']),
        ]

    def __str__(self):
        return f"{self.numero_factura} - {self.get_estado_display()} - ${self.total:.2f}"

    def clean(self):
        """
        Validaciones adicionales antes de guardar el modelo
        """
        # Validar que no exista otra factura para el mismo pedido
        if Factura.objects.exclude(pk=self.pk).filter(pedido=self.pedido).exists():
            raise ValidationError({'pedido': _('Ya existe una factura para este pedido.')})
        
        # Validar que el total sea positivo
        if self.total <= 0:
            raise ValidationError({'total': _('El total debe ser mayor a cero.')})

    def save(self, *args, **kwargs):
        """
        Lógica personalizada al guardar la factura
        """
        # Generar número de factura si no existe
        if not self.numero_factura:
            anio_mes = timezone.now().strftime('%Y%m')
            ultima = Factura.objects.filter(
                numero_factura__startswith=f'FAC-{anio_mes}'
            ).order_by('-numero_factura').first()
            consecutivo = (int(ultima.numero_factura[-4:]) + 1 if ultima else 1)
            self.numero_factura = f"FAC-{anio_mes}-{consecutivo:04d}"
        
        # Calcular valores financieros si no están definidos
        if not self.subtotal or not self.iva:
            self.calcular_totales()
        
        # Establecer usuario creador si no está definido
        if not self.creado_por and hasattr(self, 'request_user'):
            self.creado_por = self.request_user
        
        # Establecer fecha de vencimiento por defecto (7 días después)
        if not self.fecha_vencimiento:
            self.fecha_vencimiento = timezone.now().date() + timezone.timedelta(days=7)
        
        super().save(*args, **kwargs)

    def generar_numero_factura(self):
        """
        Genera un número de factura único con formato FAC-YYYYMM-NNNN
        """
        año_mes = timezone.now().strftime('%Y%m')
        ultima_factura = Factura.objects.filter(
            numero_factura__startswith=f'FAC-{año_mes}'
        ).order_by('-numero_factura').first()
        
        consecutivo = (int(ultima_factura.numero_factura[-4:]) + 1) if ultima_factura else 1
        self.numero_factura = f"FAC-{año_mes}-{consecutivo:04d}"

    def calcular_totales(self):
        """
        Calcula automáticamente subtotal, IVA y total
        """
        if hasattr(self.pedido, 'items'):
            self.subtotal = sum(
                item.cantidad * item.precio_unitario 
                for item in self.pedido.items.all()
            )
            self.iva = self.subtotal * 0.12  # 12% de IVA
            self.total = self.subtotal + self.iva

    def anular(self, usuario=None, observaciones=None):
        """
        Método para anular una factura
        """
        if self.estado == self.EstadoFactura.ANULADA:
            raise ValidationError(_('La factura ya está anulada'))
        
        self.estado = self.EstadoFactura.ANULADA
        if observaciones:
            self.observaciones = observaciones
        if usuario:
            self.creado_por = usuario
        self.save()

    @property
    def esta_pagada(self):
        return self.estado == self.EstadoFactura.PAGADA
    
    @property
    def esta_anulada(self):
        return self.estado == self.EstadoFactura.ANULADA
    
    @property
    def esta_vencida(self):
        if self.fecha_vencimiento:
            return not self.esta_pagada and self.fecha_vencimiento < timezone.now().date()
        return False