# Importar los módulos necesarios de Django REST Framework (DRF).
from rest_framework import serializers

# Importar los modelos Pedido e ItemPedido desde el archivo models.py.
from .models import Pedido, ItemPedido

class ItemPedidoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ItemPedido.
    Convierte los objetos ItemPedido en JSON y viceversa.
    """
    class Meta:
        """
        Clase Meta para configurar el serializador.
        """
        model = ItemPedido  # Especifica el modelo que se va a serializar.
        fields = ['producto', 'cantidad', 'precio_unitario']  # Campos que se incluirán en el JSON.

class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Pedido.
    Convierte los objetos Pedido en JSON y viceversa.
    Incluye los ítems asociados al pedido.
    """
    # Campo 'items' que utiliza el serializador ItemPedido para incluir los ítems del pedido.
    items = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        """
        Clase Meta para configurar el serializador.
        """
        model = Pedido  # Especifica el modelo que se va a serializar.
        fields = ['id', 'usuario_id', 'fecha_creacion', 'estado', 'total', 'items']  # Campos que se incluirán en el JSON.