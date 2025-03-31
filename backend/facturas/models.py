from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from pedidos.models import Pedido
from django.core.exceptions import ValidationError
import os

class Factura(models.Model):
    """
    Modelo completo para facturas con:
    - Generación automática de números de factura
    - Relación con pedidos y usuarios
    - Gestión de archivos PDF
    - Validaciones integradas
    """
    
    # Campos principales
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID',
        help_text='Identificador único automático'
    )
    
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name='factura',
        verbose_name='Pedido asociado',
        help_text='Pedido al que pertenece esta factura'
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

    # Configuración Meta
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
        indexes = [
            models.Index(fields=['numero_factura']),
            models.Index(fields=['pedido']),
        ]
        permissions = [
            ('generar_factura', 'Puede generar facturas PDF'),
            ('descargar_factura', 'Puede descargar facturas'),
        ]

    # Métodos
    def __str__(self):
        return f"{self.numero_factura} - ${self.total}"

    def save(self, *args, **kwargs):
        """Genera número de factura y calcula total al guardar"""
        if not self.numero_factura:
            self._generar_numero_factura()
        
        if not self.total:
            self.calcular_total()
            
        self.full_clean()
        super().save(*args, **kwargs)

    def _generar_numero_factura(self):
        """Genera número de factura en formato FAC-AAAAMM-NNNN"""
        año_mes = timezone.now().strftime('%Y%m')
        ultima = Factura.objects.filter(
            numero_factura__startswith=f'FAC-{año_mes}'
        ).order_by('-numero_factura').first()
        
        if ultima:
            try:
                consecutivo = int(ultima.numero_factura[-4:]) + 1
            except ValueError:
                consecutivo = 1
        else:
            consecutivo = 1
            
        self.numero_factura = f"FAC-{año_mes}-{consecutivo:04d}"

    def calcular_total(self):
        """Calcula el total sumando los items del pedido"""
        if hasattr(self.pedido, 'items'):
            self.total = sum(
                item.cantidad * item.precio_unitario 
                for item in self.pedido.items.all()
            )
        return self.total

    def generar_nombre_pdf(self):
        """Genera nombre de archivo PDF consistente"""
        return f"factura_{self.numero_factura}.pdf"

    @property
    def datos_cliente(self):
        """Diccionario con datos estructurados del cliente"""
        return {
            'nombre': self.pedido.usuario.get_full_name(),
            'cedula': self.pedido.usuario.cedula,
            'direccion': self.pedido.usuario.direccion,
            'telefono': str(self.pedido.usuario.telefono),
            'email': self.pedido.usuario.email
        }

    def clean(self):
        """Validaciones adicionales"""
        if self.total and self.total < 0:
            raise ValidationError({'total': 'El total no puede ser negativo'})
        
        if not self.pedido:
            raise ValidationError('La factura debe estar asociada a un pedido')

    # Señales y handlers (opcional)
    @classmethod
    def post_create(cls, sender, instance, created, **kwargs):
        """Handler para señales post-create"""
        if created and not instance.numero_factura:
            instance.save()

# Conexión de señal (opcional)
from django.db.models.signals import post_save
post_save.connect(Factura.post_create, sender=Factura)