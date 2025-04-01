from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from .models import Factura
from pedidos.models import Pedido
from django.core.files.base import ContentFile
from .serializers import (
    FacturaSerializer,
    GenerarFacturaSerializer,
    FiltroFacturasSerializer,
    CambiarEstadoFacturaSerializer,
    FacturaErrorCodes
)
from django.db.models import Q
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def generar_factura(request):
    """
    Endpoint para generar una nueva factura
    Permisos requeridos: facturas.add_factura
    """
    serializer = GenerarFacturaSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            {'error': serializer.errors, 'code': FacturaErrorCodes.PEDIDO_NO_EXISTE},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if not request.user.has_perm('facturas.add_factura'):
            raise PermissionDenied

        pedido = get_object_or_404(Pedido, id=serializer.validated_data['pedido_id'])
        
        # Verificar si ya existe factura para este pedido
        if Factura.objects.filter(pedido=pedido).exists():
            factura_existente = Factura.objects.get(pedido=pedido)
            return JsonResponse(
                {
                    'error': 'Ya existe una factura para este pedido',
                    'code': FacturaErrorCodes.FACTURA_EXISTENTE,
                    'factura_id': factura_existente.id,
                    'pdf_url': request.build_absolute_uri(factura_existente.archivo_pdf.url) if factura_existente.archivo_pdf else None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear la factura
        factura = Factura(pedido=pedido, total=pedido.total)
        factura.save()

        # Generar PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        
        # Configuración del PDF
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, 800, f"FACTURA {factura.numero_factura}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 780, f"Fecha: {factura.fecha_emision.strftime('%d/%m/%Y %H:%M')}")
        pdf.drawString(100, 760, f"Cliente: {pedido.usuario.get_full_name()}")
        
        # Guardar PDF
        pdf.save()
        filename = f"factura_{factura.numero_factura}.pdf"
        factura.archivo_pdf.save(filename, ContentFile(buffer.getvalue()))
        
        # Serializar la respuesta
        factura_serializer = FacturaSerializer(factura, context={'request': request})
        return JsonResponse(factura_serializer.data, status=status.HTTP_201_CREATED)

    except PermissionDenied:
        return JsonResponse(
            {'error': 'No tiene permisos para generar facturas', 'code': FacturaErrorCodes.PERMISO_DENEGADO},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return JsonResponse(
            {'error': str(e), 'code': FacturaErrorCodes.ERROR_GENERACION_PDF},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_facturas(request):
    """
    Endpoint para listar facturas con filtros
    Permisos requeridos: facturas.view_factura o ser el dueño de la factura
    """
    try:
        filtro_serializer = FiltroFacturasSerializer(data=request.query_params)
        if not filtro_serializer.is_valid():
            return JsonResponse(filtro_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Construir queryset base
        queryset = Factura.objects.select_related('pedido__usuario').all()
        
        # Aplicar filtros
        filtros = Q()
        if 'fecha_inicio' in filtro_serializer.validated_data:
            fecha_inicio = filtro_serializer.validated_data['fecha_inicio']
            filtros &= Q(fecha_emision__gte=datetime.combine(fecha_inicio, datetime.min.time()))
        
        if 'fecha_fin' in filtro_serializer.validated_data:
            fecha_fin = filtro_serializer.validated_data['fecha_fin']
            filtros &= Q(fecha_emision__lte=datetime.combine(fecha_fin, datetime.max.time()))
        
        if 'cliente' in filtro_serializer.validated_data:
            cliente = filtro_serializer.validated_data['cliente']
            filtros &= Q(pedido__usuario__nombre_completo__icontains=cliente)
        
        if 'pedido_id' in filtro_serializer.validated_data:
            filtros &= Q(pedido__id=filtro_serializer.validated_data['pedido_id'])
        
        if 'estado' in filtro_serializer.validated_data:
            filtros &= Q(estado=filtro_serializer.validated_data['estado'])

        queryset = queryset.filter(filtros)

        # Verificar permisos para cada factura
        if not request.user.has_perm('facturas.view_all_facturas'):
            queryset = queryset.filter(pedido__usuario=request.user)

        serializer = FacturaSerializer(queryset, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    except Exception as e:
        return JsonResponse(
            {'error': str(e), 'code': FacturaErrorCodes.ERROR_GENERACION_PDF},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_factura(request, factura_id):
    """
    Endpoint para ver el detalle de una factura específica
    """
    try:
        factura = get_object_or_404(Factura, id=factura_id)
        
        # Verificar permisos
        if not (request.user.has_perm('facturas.view_all_facturas') or 
                factura.pedido.usuario == request.user):
            raise PermissionDenied

        serializer = FacturaSerializer(factura, context={'request': request})
        return JsonResponse(serializer.data)

    except PermissionDenied:
        return JsonResponse(
            {'error': 'No tiene permisos para ver esta factura', 'code': FacturaErrorCodes.PERMISO_DENEGADO},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return JsonResponse(
            {'error': str(e), 'code': FacturaErrorCodes.ERROR_GENERACION_PDF},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cambiar_estado_factura(request, factura_id):
    """
    Endpoint para cambiar el estado de una factura
    Permisos requeridos: facturas.change_estado_factura
    """
    try:
        factura = get_object_or_404(Factura, id=factura_id)
        
        if not request.user.has_perm('facturas.change_estado_factura'):
            raise PermissionDenied

        serializer = CambiarEstadoFacturaSerializer(data=request.data, context={'instance': factura})
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        factura.estado = serializer.validated_data['estado']
        factura.save()
        
        return JsonResponse(
            FacturaSerializer(factura, context={'request': request}).data,
            status=status.HTTP_200_OK
        )

    except PermissionDenied:
        return JsonResponse(
            {'error': 'No tiene permisos para cambiar el estado de facturas', 'code': FacturaErrorCodes.PERMISO_DENEGADO},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return JsonResponse(
            {'error': str(e), 'code': FacturaErrorCodes.ERROR_GENERACION_PDF},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def descargar_factura_pdf(request, factura_id):
    """
    Endpoint para descargar el PDF de una factura
    """
    try:
        factura = get_object_or_404(Factura, id=factura_id)
        
        # Verificar permisos
        if not (request.user.has_perm('facturas.view_all_facturas') or 
                factura.pedido.usuario == request.user):
            raise PermissionDenied

        if not factura.archivo_pdf:
            return JsonResponse(
                {'error': 'La factura no tiene PDF generado', 'code': 1005},
                status=status.HTTP_404_NOT_FOUND
            )

        with open(factura.archivo_pdf.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="factura_{factura.numero_factura}.pdf"'
            return response

    except PermissionDenied:
        return JsonResponse(
            {'error': 'No tiene permisos para descargar esta factura', 'code': FacturaErrorCodes.PERMISO_DENEGADO},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return JsonResponse(
            {'error': str(e), 'code': FacturaErrorCodes.ERROR_GENERACION_PDF},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )