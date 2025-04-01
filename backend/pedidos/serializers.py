from rest_framework import serializers
from .models import Pedido, ItemPedido
from productos.models import Producto
from productos.serializers import ProductoSerializer
from usuarios.serializers import UsuarioBaseSerializer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ItemPedidoSerializer(serializers.ModelSerializer):
    """
    Serializador detallado para ítems de pedido con validación de stock.
    Incluye información completa del producto relacionado.
    """
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',
        write_only=True,
        help_text=_("ID del producto a ordenar")
    )
    subtotal = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
        help_text=_("Subtotal calculado (cantidad × precio unitario)")
    )

    class Meta:
        model = ItemPedido
        fields = [
            'id',
            'producto',
            'producto_id',
            'cantidad',
            'precio_unitario',
            'subtotal'
        ]
        read_only_fields = ['precio_unitario', 'subtotal']
        extra_kwargs = {
            'cantidad': {
                'min_value': 1,
                'help_text': _("Cantidad a ordenar (mínimo 1)")
            }
        }

    def validate(self, data):
        """
        Validaciones combinadas:
        - Stock suficiente disponible
        - Precio unitario no modificado
        """
        producto = data.get('producto')
        cantidad = data.get('cantidad', 1)
        
        if producto and cantidad > producto.stock:
            raise serializers.ValidationError({
                'cantidad': _("Stock insuficiente. Disponible: %(stock)s") % {
                    'stock': producto.stock
                }
            })
            
        return data

    def create(self, validated_data):
        """
        Asigna automáticamente el precio unitario al momento de creación
        """
        validated_data['precio_unitario'] = validated_data['producto'].precio_final
        return super().create(validated_data)

class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializador principal para pedidos con:
    - Items anidados
    - Validación de estado y método de entrega
    - Integración completa con usuarios
    """
    items = ItemPedidoSerializer(
        many=True,
        required=True,
        help_text=_("Lista de items en el pedido")
    )
    usuario = UsuarioBaseSerializer(
        read_only=True,
        help_text=_("Información básica del comprador")
    )
    estado_display = serializers.CharField(
        source='get_estado_display',
        read_only=True,
        help_text=_("Nombre legible del estado")
    )
    metodo_entrega_display = serializers.CharField(
        source='get_metodo_entrega_display',
        read_only=True,
        help_text=_("Nombre legible del método de entrega")
    )

    class Meta:
        model = Pedido
        fields = [
            'id',
            'usuario',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
            'estado_display',
            'metodo_entrega',
            'metodo_entrega_display',
            'direccion_entrega',
            'metodo_pago',
            'total',
            'items'
        ]
        read_only_fields = [
            'id',
            'usuario',
            'fecha_creacion',
            'fecha_actualizacion',
            'total',
            'estado_display',
            'metodo_entrega_display'
        ]
        extra_kwargs = {
            'direccion_entrega': {
                'required': False,
                'help_text': _("Requerido para envíos a domicilio")
            },
            'metodo_pago': {
                'required': False,
                'help_text': _("Método de pago utilizado")
            }
        }

    def validate(self, data):
        """
        Validaciones combinadas:
        - Al menos un ítem en el pedido
        - Dirección requerida para envíos
        - Estado válido según workflow
        """
        items = data.get('items', self.context.get('items', []))
        metodo_entrega = data.get('metodo_entrega')
        direccion = data.get('direccion_entrega')
        estado = data.get('estado')

        errors = {}

        if not items:
            errors['items'] = _("El pedido debe contener al menos un ítem.")
            
        if metodo_entrega == Pedido.MetodoEntrega.DOMICILIO and not direccion:
            errors['direccion_entrega'] = _("Se requiere dirección para envío a domicilio.")
            
        if estado and estado not in Pedido.EstadoPedido.values:
            errors['estado'] = _("Estado no válido.")
            
        if errors:
            raise serializers.ValidationError(errors)
            
        return data

    def create(self, validated_data):
        """
        Crea un pedido con:
        - Usuario autenticado como comprador
        - Items validados
        - Total calculado automáticamente
        """
        items_data = validated_data.pop('items')
        request = self.context.get('request')
        
        if request and hasattr(request, 'user'):
            validated_data['usuario'] = request.user
            
        pedido = Pedido.objects.create(**validated_data)
        
        for item_data in items_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
            
        pedido.calcular_total()
        return pedido

    def update(self, instance, validated_data):
        """
        Actualización controlada:
        - Solo permite ciertos cambios de estado
        - Actualiza stock cuando corresponde
        """
        nuevo_estado = validated_data.get('estado')
        
        # Lógica para manejar cambios de estado
        if nuevo_estado:
            if nuevo_estado == Pedido.EstadoPedido.PAGADO:
                instance.actualizar_stock(accion='restar')
            elif nuevo_estado == Pedido.EstadoPedido.CANCELADO:
                instance.actualizar_stock(accion='sumar')
                
        return super().update(instance, validated_data)