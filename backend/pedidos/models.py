"""
Modelos para la gestión de pedidos en el sistema e-commerce.
Este archivo define la estructura de la base de datos para:
- Pedidos (tabla principal)
- Ítems de pedido (tabla relacionada)

Conecta con otras apps del proyecto:
- usuarios: Para saber qué usuario hizo el pedido
- productos: Para saber qué productos se compraron
- facturas: Para generar la factura automáticamente
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum, F  # F permite hacer operaciones con campos de la BD
from django.db import transaction  # Para operaciones atómicas
from productos.models import Producto
from usuarios.models import Usuario
from facturas.models import Factura

class Pedido(models.Model):
    """
    Modelo que representa un pedido completo hecho por un usuario.
    Un pedido contiene:
    - Usuario que lo hizo
    - Varios ítems (productos)
    - Estado actual
    - Total a pagar
    - Factura asociada (opcional)
    """

    # Los posibles estados por los que puede pasar un pedido
    ESTADOS = (
        ('pendiente', 'Pendiente'),  # Primer valor se guarda en BD, segundo es legible
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    
    # Relación con el modelo Usuario (de la app usuarios)
    # on_delete=CASCADE significa que si se borra el usuario, se borran sus pedidos
    # related_name permite acceder a los pedidos desde un usuario: usuario.pedidos.all()
    usuario = models.ForeignKey(
        Usuario,  # Modelo con el que se relaciona
        on_delete=models.CASCADE,  # Comportamiento al borrar
        related_name='pedidos',  # Nombre para la relación inversa
        verbose_name='Usuario'  # Nombre legible en el admin
    )
    
    # Fecha automática cuando se crea (no se modifica)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,  # Se establece solo al crear
        verbose_name='Fecha de creación'
    )
    
    # Fecha que se actualiza automáticamente al guardar cambios
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,  # Se actualiza en cada guardado
        verbose_name='Última actualización'
    )
    
    # Estado actual del pedido, usa las opciones definidas en ESTADOS
    estado = models.CharField(
        max_length=20,  # Longitud máxima en BD
        choices=ESTADOS,  # Opciones disponibles
        default='pendiente',  # Valor por defecto
        verbose_name='Estado del pedido'
    )
    
    # Total calculado del pedido (suma de todos los ítems)
    total = models.DecimalField(
        max_digits=12,  # Número máximo de dígitos (incluyendo decimales)
        decimal_places=2,  # Decimales a guardar
        default=0.00,  # Valor inicial
        verbose_name='Total del pedido'
    )
    
    # Relación con la factura (de la app facturas)
    # OneToOne porque cada pedido tiene UNA factura y viceversa
    factura = models.OneToOneField(
        Factura,  # Modelo relacionado
        on_delete=models.SET_NULL,  # Si se borra la factura, no se borra el pedido
        null=True,  # Puede ser NULL en BD
        blank=True,  # Puede estar vacío en formularios
        related_name='pedido',  # Para acceder al pedido desde la factura
        verbose_name='Factura asociada'
    )

    class Meta:
        """
        Clase Meta para configuraciones adicionales del modelo.
        """
        verbose_name = 'Pedido'  # Nombre singular en el admin
        verbose_name_plural = 'Pedidos'  # Nombre plural en el admin
        ordering = ['-fecha_creacion']  # Orden por defecto (más nuevos primero)
        indexes = [  # Índices para acelerar búsquedas
            models.Index(fields=['usuario']),  # Buscar por usuario
            models.Index(fields=['estado']),  # Buscar por estado
            models.Index(fields=['fecha_creacion']),  # Buscar por fecha
        ]

    def __str__(self):
        """
        Método mágico que define cómo se convierte el objeto a string.
        Se usa en el admin de Django y cuando imprimes el objeto.
        """
        return f"Pedido #{self.id} - {self.usuario.email} ({self.get_estado_display()}) - ${self.total}"

    def calcular_total(self):
        """
        Calcula el total sumando todos los ítems del pedido.
        Usa agregación a nivel de base de datos para mejor rendimiento.
        """
        # Suma en la BD: cantidad * precio_unitario para todos los ítems
        resultado = self.items.aggregate(
            total=Sum(F('cantidad') * F('precio_unitario'))
        # Actualiza el total (usa 0.00 si no hay resultado)
        self.total = resultado['total'] or 0.00
        # Guarda solo el campo total (optimización)
        self.save(update_fields=['total'])
        return self.total

    def generar_factura(self):
        """
        Crea una factura asociada al pedido automáticamente.
        Conecta con la app facturas.
        """
        if not self.factura:  # Si no tiene factura aún
            # Crea la factura en la base de datos
            factura = Factura.objects.create(
                usuario=self.usuario,  # El mismo usuario del pedido
                pedido=self,  # Este mismo pedido
                total=self.total,  # El total calculado
                estado='pendiente'  # Estado inicial
            )
            self.factura = factura  # Asigna la nueva factura
            self.save()  # Guarda el cambio
        return self.factura  # Devuelve la factura (nueva o existente)

    def cancelar(self):
        """
        Cancela el pedido y devuelve el stock a los productos.
        Usa transacción atómica para evitar inconsistencias.
        """
        if self.estado != 'cancelado':  # Si no está ya cancelado
            with transaction.atomic():  # Bloque transaccional
                # Recorre todos los ítems del pedido
                for item in self.items.select_related('producto').select_for_update():
                    producto = item.producto
                    # Devuelve el stock
                    producto.stock += item.cantidad
                    producto.save()  # Guarda el producto
                
                # Actualiza el estado
                self.estado = 'cancelado'
                self.save(update_fields=['estado'])  # Guarda solo el estado
                
                # Si tiene factura, la cancela también
                if self.factura:
                    self.factura.actualizar_estado('cancelada')

    def clean(self):
        """
        Método de validación que Django ejecuta automáticamente.
        Se usa en forms y en el admin.
        """
        if self.pk and self.items.count() == 0:  # Si ya existe y no tiene ítems
            raise ValidationError("El pedido debe tener al menos un ítem.")

class ItemPedido(models.Model):
    """
    Modelo que representa un producto específico dentro de un pedido.
    Contiene:
    - Pedido al que pertenece
    - Producto comprado
    - Cantidad comprada
    - Precio en el momento de la compra
    """

    # Relación con el pedido padre
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,  # Si se borra el pedido, se borran sus ítems
        related_name='items',  # Para acceder desde pedido: pedido.items.all()
        verbose_name='Pedido'
    )
    
    # Relación con el producto comprado
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,  # Evita borrar productos con pedidos activos
        related_name='pedidos',  # Para acceder desde producto: producto.pedidos.all()
        verbose_name='Producto'
    )
    
    # Cantidad comprada (entero positivo)
    cantidad = models.PositiveIntegerField(
        default=1,  # Valor por defecto
        verbose_name='Cantidad'
    )
    
    # Precio en el momento de la compra (para mantener histórico)
    precio_unitario = models.DecimalField(
        max_digits=10,  # Máximo 10 dígitos
        decimal_places=2,  # 2 decimales
        verbose_name='Precio unitario'
    )
    
    # Fecha de creación automática
    creado_en = models.DateTimeField(
        auto_now_add=True,  # Solo se establece al crear
        verbose_name='Fecha de creación'
    )

    class Meta:
        """Configuraciones adicionales para los ítems"""
        verbose_name = 'Ítem de pedido'
        verbose_name_plural = 'Ítems de pedido'
        constraints = [  # Restricciones de base de datos
            # No puede haber el mismo producto dos veces en un pedido
            models.UniqueConstraint(
                fields=['pedido', 'producto'],  # Campos que deben ser únicos juntos
                name='unique_producto_en_pedido'  # Nombre de la restricción
            )
        ]

    def __str__(self):
        """Representación en texto del ítem"""
        return f"{self.cantidad}x {self.producto.nombre} (${self.precio_unitario} c/u)"

    def subtotal(self):
        """Calcula el subtotal (cantidad x precio unitario)"""
        return self.cantidad * self.precio_unitario

    def clean(self):
        """
        Validaciones automáticas que hace Django:
        1. Cantidad debe ser positiva
        2. Debe haber suficiente stock
        3. El precio debe coincidir con el producto
        """
        # Validación 1: Cantidad positiva
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")
            
        # Validación 2: Stock suficiente (solo para nuevos ítems)
        if not self.pk:  # pk es None cuando es nuevo (no guardado aún)
            if self.cantidad > self.producto.stock:
                raise ValidationError(
                    f"Stock insuficiente. Disponible: {self.producto.stock}"
                )
            
            # Validación 3: Precio debe ser el actual del producto
            if self.precio_unitario != self.producto.precio:
                self.precio_unitario = self.producto.precio  # Corrige automáticamente

    def save(self, *args, **kwargs):
        """
        Método que se ejecuta al guardar el ítem.
        *args y **kwargs permiten recibir argumentos variables que Django envía.
        
        Hace tres cosas:
        1. Ejecuta las validaciones con clean()
        2. Actualiza el stock del producto (si es nuevo ítem)
        3. Actualiza el total del pedido
        """
        # 1. Ejecuta validaciones
        self.clean()
        
        # Bloque transaccional (todo o nada)
        with transaction.atomic():
            # 2. Actualiza stock solo para nuevos ítems
            if not self.pk:  # Si no tiene primary key (no está guardado aún)
                # Bloquea el producto para evitar race conditions
                producto = Producto.objects.select_for_update().get(pk=self.producto.pk)
                producto.stock -= self.cantidad  # Reduce el stock
                producto.save()  # Guarda el producto
            
            # 3. Guarda el ítem (llama al save original de models.Model)
            super().save(*args, **kwargs)
            # Actualiza el total del pedido padre
            self.pedido.calcular_total()

    def delete(self, *args, **kwargs):
        """
        Método que se ejecuta al borrar el ítem.
        *args y **kwargs permiten recibir argumentos variables que Django envía.
        
        Hace dos cosas:
        1. Devuelve el stock al producto
        2. Actualiza el total del pedido
        """
        # Bloque transaccional (todo o nada)
        with transaction.atomic():
            # 1. Devuelve el stock
            producto = self.producto
            producto.stock += self.cantidad
            producto.save()
            
            # Guarda referencia al pedido antes de borrar
            pedido = self.pedido
            # 2. Borra el ítem (llama al delete original de models.Model)
            super().delete(*args, **kwargs)
            # Actualiza el total del pedido
            pedido.calcular_total()