from rest_framework import serializers
from .models import Factura
from pedidos.models import Pedido, ItemPedido

# Serializer para los ítems del pedido
class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']
        read_only_fields = ['id']  # Hace que el campo 'id' sea de solo lectura

# Serializer para el pedido
class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)  # Incluye los ítems del pedido

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'fecha', 'items']
        read_only_fields = ['id', 'fecha']  # Hace que 'id' y 'fecha' sean de solo lectura

# Serializer para la factura
class FacturaSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)  # Incluye los detalles del pedido

    class Meta:
        model = Factura
        fields = ['factura_id', 'pedido', 'fecha_emision', 'total']
        read_only_fields = ['factura_id', 'fecha_emision', 'total']  # Hace que estos campos sean de solo lectura