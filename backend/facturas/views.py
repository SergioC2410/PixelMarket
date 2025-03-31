from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Factura
from pedidos.models import Pedido
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from datetime import datetime
from django.core.files.base import ContentFile

@csrf_exempt
def generar_factura(request, pedido_id):
    """Genera factura en PDF y guarda en el modelo"""
    try:
        pedido = get_object_or_404(Pedido.objects.select_related('usuario'), id=pedido_id)
        factura, created = Factura.objects.get_or_create(
            pedido=pedido,
            defaults={'total': pedido.total}
        )

        # Generar PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        
        # Contenido del PDF (personalizable)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, 800, f"FACTURA {factura.numero_factura}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 770, f"Cliente: {pedido.usuario.nombre_completo()}")
        # ... (agrega más contenido como en ejemplos anteriores)

        pdf.save()
        
        # Guardar PDF
        filename = f"factura_{factura.numero_factura}.pdf"
        factura.archivo_pdf.save(filename, ContentFile(buffer.getvalue()))
        
        return HttpResponse(buffer.getvalue(), content_type='application/pdf')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def listar_facturas(request):
    """Lista todas las facturas"""
    facturas = Factura.objects.select_related('pedido__usuario').all()
    data = [{
        'id': f.id,
        'numero_factura': f.numero_factura,
        'fecha': f.fecha_emision.strftime('%Y-%m-%d'),
        'total': float(f.total),
        'cliente': f.pedido.usuario.nombre_completo()
    } for f in facturas]
    return JsonResponse(data, safe=False)

@csrf_exempt
def detalle_factura(request, factura_id):
    """Detalle completo de una factura"""
    factura = get_object_or_404(Factura.objects.select_related('pedido__usuario'), id=factura_id)
    data = {
        'numero_factura': factura.numero_factura,
        'fecha': factura.fecha_emision.strftime('%Y-%m-%d %H:%M'),
        'total': float(factura.total),
        'cliente': {
            'nombre': factura.pedido.usuario.nombre_completo(),
            'cedula': factura.pedido.usuario.cedula,
            'email': factura.pedido.usuario.email
        },
        'pdf_url': request.build_absolute_uri(factura.archivo_pdf.url) if factura.archivo_pdf else None
    }
    return JsonResponse(data)

@csrf_exempt
def descargar_factura_pdf(request, factura_id):
    """Descarga directa del PDF"""
    factura = get_object_or_404(Factura, id=factura_id)
    if not factura.archivo_pdf:
        return JsonResponse({'error': 'PDF no generado'}, status=404)
    
    with open(factura.archivo_pdf.path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.numero_factura}.pdf"'
        return response