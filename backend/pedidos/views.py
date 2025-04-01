from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from productos.models import Producto
from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer
from usuarios.permissions import EsPropietario

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, EsPropietario]

    def get_queryset(self):
        # Filtra los pedidos por el usuario autenticado
        return self.queryset.filter(usuario=self.request.user)
class PedidoListCreateView(generics.ListCreateAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all().select_related('usuario').prefetch_related('items')

    def get_queryset(self):
        # Filtrar los pedidos por el usuario logueado
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Crear un pedido y actualizar el stock
        with transaction.atomic():
            pedido = serializer.save(usuario=self.request.user)
            self.actualizar_stock(pedido, accion='reservar')

    def actualizar_stock(self, pedido, accion):
        # Actualizar el stock de los productos en el pedido
        for item in pedido.items.all():
            if accion == 'reservar':
                item.producto.reducir_stock(item.cantidad)
            elif accion == 'liberar':
                item.producto.aumentar_stock(item.cantidad)
            elif accion == 'confirmar':
                item.producto.reducir_stock(item.cantidad)
            elif accion == 'restar':
                item.producto.reducir_stock(item.cantidad)
            elif accion == 'sumar':
                item.producto.aumentar_stock(item.cantidad)


class PedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, EsPropietario]
    queryset = Pedido.objects.all().select_related('usuario').prefetch_related('items')

    def perform_update(self, serializer):
        old_status = self.get_object().estado
        new_status = serializer.validated_data.get('estado', old_status)

        with transaction.atomic():
            pedido = serializer.save()
            self.manejar_cambio_estado(pedido, old_status, new_status)

    def perform_destroy(self, instance):
        # Actualizar stock al eliminar el pedido
        with transaction.atomic():
            self.actualizar_stock(instance, accion='liberar')
            instance.delete()

    def manejar_cambio_estado(self, pedido, old_status, new_status):
        if new_status == Pedido.EstadoPedido.CANCELADO:
            self.actualizar_stock(pedido, accion='liberar')
        elif new_status == Pedido.EstadoPedido.PAGADO and old_status != new_status:
            self.actualizar_stock(pedido, accion='confirmar')


@api_view(['POST'])
@permission_classes([IsAuthenticated, EsPropietario])
def cancelar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.estado == Pedido.EstadoPedido.REEMBOLSADO:
        return Response(
            {'error': 'No se puede cancelar un pedido ya reembolsado.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        pedido.estado = Pedido.EstadoPedido.CANCELADO
        pedido.save()
        # Actualizar stock al cancelar el pedido
        pedido.actualizar_stock(accion='sumar')

    return Response(
        {'mensaje': 'Pedido cancelado exitosamente.'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated, EsPropietario])
def marcar_como_pagado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.estado != Pedido.EstadoPedido.PENDIENTE_PAGO:
        return Response(
            {'error': 'Solo se pueden marcar como pagados pedidos en estado Pendiente de Pago.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        pedido.estado = Pedido.EstadoPedido.PAGADO
        pedido.save()
        # Actualizar stock al marcar como pagado
        pedido.actualizar_stock(accion='restar')

    return Response(
        {'mensaje': 'Pedido marcado como pagado exitosamente.'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated, EsPropietario])
def reembolsar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.estado not in [Pedido.EstadoPedido.CANCELADO, Pedido.EstadoPedido.PAGADO]:
        return Response(
            {'error': 'Solo se pueden reembolsar pedidos cancelados o pagados.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        pedido.estado = Pedido.EstadoPedido.REEMBOLSADO
        pedido.save()
        # Actualizar stock al reembolsar
        if pedido.estado == Pedido.EstadoPedido.PAGADO:
            pedido.actualizar_stock(accion='sumar')

    return Response(
        {'mensaje': 'Pedido reembolsado exitosamente.'},
        status=status.HTTP_200_OK
    )
