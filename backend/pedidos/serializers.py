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

    def validate_cantidad(self, value):
        """
        Valida que la cantidad no sea negativa o cero.
        """
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero.")
        return value

    def validate(self, data):
        """
        Valida que la cantidad no exceda el stock disponible del producto.
        """
        producto = data['producto']
        cantidad = data['cantidad']
        if cantidad > producto.stock:
            raise serializers.ValidationError(f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")
        return data

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
        fields = ['id', 'usuario_id', 'fecha_creacion', 'estado', 'metodo_entrega', 
                 'direccion_entrega', 'total', 'items']  # Campos que se incluirán en el JSON.

    def validate_estado(self, value):
        """
        Valida que el estado del pedido sea uno de los permitidos.
        """
        estados_permitidos = [estado[0] for estado in Pedido.ESTADOS]
        if value not in estados_permitidos:
            raise serializers.ValidationError(f"Estado no válido. Los estados permitidos son: {', '.join(estados_permitidos)}")
        return value

    def validate_metodo_entrega(self, value):
        """
        Valida que el método de entrega sea uno de los permitidos.
        """
        metodos_permitidos = [metodo[0] for metodo in Pedido.METODOS_ENTREGA]
        if value not in metodos_permitidos:
            raise serializers.ValidationError(f"Método de entrega no válido. Los métodos permitidos son: {', '.join(metodos_permitidos)}")
        return value

    def validate(self, data):
        """
        Valida que el pedido tenga al menos un ítem antes de guardarlo.
        Valida también que si el método de entrega es a domicilio, haya una dirección.
        """
        if 'items' not in self.context or len(self.context['items']) == 0:
            raise serializers.ValidationError("El pedido debe contener al menos un ítem.")
            
        if data.get('metodo_entrega') == 'domicilio' and not data.get('direccion_entrega'):
            raise serializers.ValidationError("Debe proporcionar una dirección de entrega para envío a domicilio.")
            
        return data