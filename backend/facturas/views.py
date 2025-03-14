# Este archivo contiene la lógica para manejar las solicitudes HTTP (APIs) y generar facturas en PDF usando ReportLab.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Factura
from pedidos.models import Pedido
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

@csrf_exempt
def generar_factura(request, pedido_id):
    """
    Vista para generar una factura en PDF para un pedido específico.
    """
    if request.method == 'GET':
        try:
            # Obtener el pedido
            pedido = Pedido.objects.get(id=pedido_id)

            # Crear la factura
            factura = Factura.objects.create(
                pedido=pedido,
                total=pedido.total
            )

            # Crear un buffer para el PDF
            buffer = io.BytesIO()

            # Crear el PDF con ReportLab
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 12)

            # Encabezado de la factura
            pdf.drawString(100, 750, f"Factura #{factura.id}")
            pdf.drawString(100, 730, f"Fecha de emisión: {factura.fecha_emision}")
            pdf.drawString(100, 710, f"Pedido #{pedido.id}")
            pdf.drawString(100, 690, f"Cliente: {pedido.usuario.username}")

            # Detalles de los ítems
            y = 650
            pdf.drawString(100, y, "Detalles del pedido:")
            y -= 20
            for item in pedido.items.all():
                pdf.drawString(120, y, f"{item.cantidad}x {item.producto.nombre} - ${item.precio_unitario} c/u")
                y -= 20

            # Total
            pdf.drawString(100, y - 20, f"Total: ${factura.total}")

            # Finalizar el PDF
            pdf.showPage()
            pdf.save()

            # Devolver el PDF como respuesta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def listar_facturas(request):
    """
    Vista para listar todas las facturas.
    """
    if request.method == 'GET':
        facturas = Factura.objects.all()
        facturas_data = [{
            'id': factura.id,
            'pedido_id': factura.pedido.id,
            'fecha_emision': factura.fecha_emision,
            'total': str(factura.total)
        } for factura in facturas]
        return JsonResponse(facturas_data, safe=False)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Mejoras sugeridas:
# 1. Agregar paginación para la lista de facturas.
# 2. Implementar filtros (ej: por fecha, cliente).
# 3. Agregar pruebas unitarias para cada vista.