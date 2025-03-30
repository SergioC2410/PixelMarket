"""
Serializadores para la app de pedidos.

Transforman los modelos de Django en JSON (y viceversa) para la API REST.
Conectan con los modelos: Pedido, ItemPedido, Producto (de productos) y Usuario (de usuarios).
"""

from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Pedido, ItemPedido
from productos.models import Producto
from productos.serializers import ProductoSerializer  # Para anidar productos si es necesario
from usuarios.models import Usuario

class ItemPedidoSerializer(serializers.ModelSerializer):
    """
    Serializador para los ítems de pedido.
    
    Campos incluidos:
    - producto: ID del producto (PrimaryKeyRelatedField)
    - cantidad: Cantidad comprada
    - precio_unitario: Precio en el momento de la compra
    - subtotal: Campo calculado (no se guarda en BD)
    
    Validaciones:
    - Cantidad positiva
    - Stock suficiente
    - Precio coincide con producto
    """
    
    # Mostrar solo el ID del producto (optimización)
    producto = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        error_messages={
            'does_not_exist': 'El producto con ID {pk_value} no existe.',
            'incorrect_type': 'El ID del producto debe ser un número entero.'
        }
    )
    
    # Campo de solo lectura para mostrar el subtotal
    subtotal = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
        extra_kwargs = {
            'precio_unitario': {'read_only': True}  # El precio se establece automáticamente
        }

    def get_subtotal(self, obj):
        """Calcula el subtotal (cantidad x precio_unitario)"""
        return obj.cantidad * obj.precio_unitario

    def validate_cantidad(self, value):
        """Valida que la cantidad sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero.")
        return value

    def validate(self, data):
        """
        Validaciones a nivel de objeto:
        1. Stock suficiente
        2. Precio actual del producto
        """
        producto = data['producto']
        cantidad = data.get('cantidad', 1)
        
        # Validación de stock (solo para creación)
        if not self.instance and cantidad > producto.stock:
            raise serializers.ValidationError(
                f"No hay suficiente stock para {producto.nombre}. Disponible: {producto.stock}"
            )
        
        # Asegurar que el precio es el actual del producto
        data['precio_unitario'] = producto.precio
        
        return data

class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializador principal para los pedidos.
    
    Campos incluidos:
    - id: Identificador único
    - usuario: ID del usuario
    - estado: Estado actual del pedido
    - total: Total calculado
    - fecha_creacion: Fecha de creación
    - items: Lista de ítems (usando ItemPedidoSerializer)
    - items_data: Campo especial para creación (write-only)
    
    Validaciones:
    - Estado válido
    - Pedido no vacío (para creación)
    """
    
    # Para leer los ítems existentes
    items = ItemPedidoSerializer(many=True, read_only=True)
    
    # Para recibir datos de ítems al crear/modificar (no se muestra al leer)
    items_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        help_text="Lista de ítems para creación/actualización. Formato: [{'producto': ID, 'cantidad': N}]"
    )
    
    # Información básica del usuario (solo lectura)
    usuario_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id',
            'usuario',
            'usuario_info',
            'estado',
            'total',
            'fecha_creacion',
            'fecha_actualizacion',
            'items',
            'items_data'
        ]
        extra_kwargs = {
            'usuario': {'read_only': True},  # El usuario se toma del request
            'total': {'read_only': True},
            'fecha_creacion': {'read_only': True},
            'fecha_actualizacion': {'read_only': True}
        }

    def get_usuario_info(self, obj):
        """Devuelve información básica del usuario"""
        return {
            'id': obj.usuario.id,
            'email': obj.usuario.email,
            'nombre_completo': obj.usuario.get_full_name()
        }

    def validate_estado(self, value):
        """Valida que el estado sea uno de los permitidos"""
        estados_permitidos = [estado[0] for estado in Pedido.ESTADOS]
        if value not in estados_permitidos:
            raise serializers.ValidationError(
                f"Estado inválido. Opciones válidas: {', '.join(estados_permitidos)}"
            )
        return value

    def validate(self, data):
        """
        Validaciones a nivel de objeto:
        1. Para creación: debe tener items
        2. El usuario no puede cambiarse
        """
        # Validación para creación
        if self.instance is None and not data.get('items_data'):
            raise serializers.ValidationError(
                "Para crear un pedido debe incluir items_data con los productos."
            )
        
        # El usuario no puede modificarse
        if self.instance and 'usuario' in data:
            raise serializers.ValidationError("No puede cambiar el usuario de un pedido existente.")
        
        return data

    def create(self, validated_data):
        """
        Crea un pedido con sus ítems.
        items_data debe ser una lista de diccionarios con:
        - producto: ID del producto
        - cantidad: Cantidad deseada
        """
        items_data = validated_data.pop('items_data', [])
        usuario = self.context['request'].user
        
        with transaction.atomic():
            # Crear el pedido
            pedido = Pedido.objects.create(usuario=usuario, **validated_data)
            
            # Crear los ítems
            for item_data in items_data:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item_data['producto'],
                    cantidad=item_data['cantidad'],
                    precio_unitario=item_data['producto'].precio
                )
            
            # Calcular el total
            pedido.calcular_total()
        
        return pedido

    def update(self, instance, validated_data):
        """
        Actualiza un pedido existente.
        Solo permite cambiar el estado y los ítems (si se proporcionan items_data).
        """
        items_data = validated_data.pop('items_data', None)
        
        with transaction.atomic():
            # Actualizar campos básicos
            instance = super().update(instance, validated_data)
            
            # Actualizar ítems si se proporcionaron
            if items_data is not None:
                # Eliminar ítems existentes
                instance.items.all().delete()
                
                # Crear nuevos ítems
                for item_data in items_data:
                    ItemPedido.objects.create(
                        pedido=instance,
                        producto=item_data['producto'],
                        cantidad=item_data['cantidad'],
                        precio_unitario=item_data['producto'].precio
                    )
                
                # Recalcular total
                instance.calcular_total()
        
        return instance

class PedidoResumenSerializer(serializers.ModelSerializer):
    """
    Serializador ligero para listados o resúmenes de pedidos.
    Incluye solo información básica para optimizar rendimiento.
    """
    usuario_info = serializers.SerializerMethodField()
    cantidad_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Pedido
        fields = [
            'id',
            'estado',
            'total',
            'fecha_creacion',
            'usuario_info',
            'cantidad_items'
        ]
    
    def get_usuario_info(self, obj):
        return {
            'id': obj.usuario.id,
            'nombre': obj.usuario.get_full_name()
        }
    
    def get_cantidad_items(self, obj):
        return obj.items.count()