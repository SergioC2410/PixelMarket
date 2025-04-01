from rest_framework import serializers
from .models import Factura
from pedidos.models import Pedido, ItemPedido
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

class FacturaErrorCodes:
    FACTURA_EXISTENTE = 1001
    PEDIDO_NO_EXISTE = 1002
    PERMISO_DENEGADO = 1003
    ERROR_GENERACION_PDF = 1004

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
        model = Pedido.usuario.field.related_model
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
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Factura
        fields = [
            'id',
            'numero_factura',
            'pedido',
            'fecha_emision',
            'total',
            'estado',
            'estado_display',
            'pdf_url'
        ]
        read_only_fields = ['total', 'pdf_url']
    
    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.archivo_pdf and request:
            return request.build_absolute_uri(obj.archivo_pdf.url)
        return None

class GenerarFacturaSerializer(serializers.Serializer):
    pedido_id = serializers.IntegerField(
        required=True,
        help_text="ID del pedido a facturar"
    )
    
    def validate_pedido_id(self, value):
        try:
            pedido = Pedido.objects.get(id=value)
            
            if Factura.objects.filter(pedido=pedido).exists():
                raise serializers.ValidationError({
                    'code': FacturaErrorCodes.FACTURA_EXISTENTE,
                    'message': 'Ya existe una factura para este pedido',
                    'factura_id': Factura.objects.get(pedido=pedido).id
                })
                
            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                'code': FacturaErrorCodes.PEDIDO_NO_EXISTE,
                'message': 'El pedido especificado no existe'
            })

class FiltroFacturasSerializer(serializers.Serializer):
    fecha_inicio = serializers.DateField(required=False)
    fecha_fin = serializers.DateField(required=False)
    cliente = serializers.CharField(required=False)
    pedido_id = serializers.IntegerField(required=False)
    estado = serializers.ChoiceField(
        required=False,
        choices=Factura.ESTADOS,
        help_text="Filtrar por estado (P: Pagada, N: Pendiente, A: Anulada)"
    )

class CambiarEstadoFacturaSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(
        choices=Factura.ESTADOS,
        required=True,
        help_text="Nuevo estado de la factura (P: Pagada, N: Pendiente, A: Anulada)"
    )
    
    def validate_estado(self, value):
        instance = self.context.get('instance')
        if instance and instance.estado == 'A' and value != 'A':
            raise serializers.ValidationError({
                'code': 1005,
                'message': 'No se puede modificar una factura anulada'
            })
        return value