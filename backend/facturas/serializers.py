from rest_framework import serializers
from .models import Factura
from pedidos.models import Pedido, ItemPedido
from django.urls import reverse

class ItemPedidoSerializer(serializers.ModelSerializer):
    total_item = serializers.SerializerMethodField()
    
    class Meta:
        model = ItemPedido
        fields = [
            'id',
            'producto',
            'cantidad',
            'precio_unitario',
            'total_item'
        ]
    
    def get_total_item(self, obj):
        return obj.cantidad * obj.precio_unitario

class UsuarioFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido.usuario.field.related_model  # Obtiene el modelo Usuario dinámicamente
        fields = [
            'id',
            'nombre_completo',
            'cedula',
            'direccion',
            'telefono',
            'email'
        ]

class PedidoFacturaSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)
    usuario = UsuarioFacturaSerializer(read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id',
            'fecha',
            'usuario',
            'items'
        ]

class FacturaSerializer(serializers.ModelSerializer):
    pedido = PedidoFacturaSerializer(read_only=True)
    pdf_url = serializers.SerializerMethodField()
    numero_factura = serializers.CharField(read_only=True)
    fecha_emision = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    
    class Meta:
        model = Factura
        fields = [
            'id',
            'numero_factura',
            'pedido',
            'fecha_emision',
            'total',
            'pdf_url'
        ]
        read_only_fields = ['total']
    
    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.archivo_pdf and request:
            return request.build_absolute_uri(obj.archivo_pdf.url)
        return None

# Serializer para generación de facturas
class GenerarFacturaSerializer(serializers.Serializer):
    pedido_id = serializers.IntegerField(
        required=True,
        help_text="ID del pedido a facturar"
    )
    
    def validate_pedido_id(self, value):
        if not Pedido.objects.filter(id=value).exists():
            raise serializers.ValidationError("El pedido especificado no existe")
        return value

# Serializer para búsqueda/filtrado
class FiltroFacturasSerializer(serializers.Serializer):
    fecha_inicio = serializers.DateField(required=False)
    fecha_fin = serializers.DateField(required=False)
    cliente = serializers.CharField(required=False)
    pedido_id = serializers.IntegerField(required=False)