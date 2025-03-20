from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, F
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Factura
from pedidos.models import Pedido
import io

# Mensaje de error para métodos no permitidos
ERROR_METHOD_NOT_ALLOWED = 'Método no permitido'

@csrf_exempt
def generar_factura(request, pedido_id):
    """
    Genera una factura en formato PDF para un pedido específico.
    """
    if request.method != 'GET':
        return JsonResponse({'error': ERROR_METHOD_NOT_ALLOWED}, status=405)

    try:
        # Obtener el pedido o retornar un error 404 si no existe
        pedido = get_object_or_404(Pedido, id=pedido_id)

        # Calcular el total de la factura basado en cantidad y precio_unitario de los ítems
        total_factura = pedido.items.aggregate(
            total=Sum(F('cantidad') * F('precio_unitario'))
        )['total'] or 0

        # Crear la factura en la base de datos
        factura = Factura.objects.create(
            pedido=pedido,
            total=total_factura
        )

        # Crear un buffer en memoria para almacenar el PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        # Generar encabezado de la factura
        pdf.drawString(100, 750, f"Factura #{factura.factura_id}")
        pdf.drawString(100, 730, f"Fecha de emisión: {factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
        pdf.drawString(100, 710, f"Pedido #{pedido.id}")
        pdf.drawString(100, 690, f"Cliente: {pedido.usuario.username}")

        # Listar los ítems del pedido
        y = 650
        pdf.drawString(100, y, "Detalles del pedido:")
        y -= 20

        for item in pedido.items.all():
            total_producto = item.cantidad * item.precio_unitario
            pdf.drawString(120, y, f"{item.cantidad}x {item.producto.nombre} - ${item.precio_unitario:.2f} c/u (Total: ${total_producto:.2f})")
            y -= 20

        # Mostrar el total de la factura
        pdf.drawString(100, y - 20, f"Total a pagar: ${total_factura:.2f}")

        # Finalizar el PDF y devolverlo como respuesta
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.factura_id}.pdf"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def listar_facturas(request):
    """
    Lista todas las facturas con filtros opcionales:
    - ?fecha=YYYY-MM-DD  (Filtra por fecha de emisión)
    - ?cliente=username   (Filtra por cliente)
    - ?pedido_id=123      (Filtra por un pedido específico)
    """
    if request.method != 'GET':
        return JsonResponse({'error': ERROR_METHOD_NOT_ALLOWED}, status=405)

    try:
        # Obtener todas las facturas
        facturas = Factura.objects.all()

        # Filtrar por parámetros si se proporcionan
        fecha = request.GET.get('fecha')
        cliente = request.GET.get('cliente')
        pedido_id = request.GET.get('pedido_id')

        if fecha:
            try:
                fecha_parsed = parse_date(fecha)
                if fecha_parsed:
                    facturas = facturas.filter(fecha_emision__date=fecha_parsed)
            except ValueError:
                return JsonResponse({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, status=400)

        if cliente:
            facturas = facturas.filter(pedido__usuario__username=cliente)

        if pedido_id:
            try:
                pedido_id = int(pedido_id)
                facturas = facturas.filter(pedido__id=pedido_id)
            except ValueError:
                return JsonResponse({'error': 'pedido_id debe ser un número entero'}, status=400)

        # Serializar los datos de las facturas
        facturas_data = [{
            'factura_id': factura.factura_id,
            'pedido_id': factura.pedido.id,
            'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d'),
            'cliente': factura.pedido.usuario.username,
            'total': str(factura.total)
        } for factura in facturas]

        return JsonResponse(facturas_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def descargar_factura_pdf(request, factura_id):
    """
    Descarga una factura existente en formato PDF.
    """
    if request.method != 'GET':
        return JsonResponse({'error': ERROR_METHOD_NOT_ALLOWED}, status=405)

    try:
        # Obtener la factura
        factura = get_object_or_404(Factura, factura_id=factura_id)

        # Crear un buffer para generar el PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        # Generar encabezado de la factura
        pdf.drawString(100, 750, f"Factura #{factura.factura_id}")
        pdf.drawString(100, 730, f"Fecha de emisión: {factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
        pdf.drawString(100, 710, f"Pedido #{factura.pedido.id}")
        pdf.drawString(100, 690, f"Cliente: {factura.pedido.usuario.username}")

        # Listar los ítems del pedido
        y = 650
        pdf.drawString(100, y, "Detalles del pedido:")
        y -= 20

        for item in factura.pedido.items.all():
            total_producto = item.cantidad * item.precio_unitario
            pdf.drawString(120, y, f"{item.cantidad}x {item.producto.nombre} - ${item.precio_unitario:.2f} c/u (Total: ${total_producto:.2f})")
            y -= 20

        # Mostrar el total de la factura
        pdf.drawString(100, y - 20, f"Total a pagar: ${factura.total:.2f}")

        # Finalizar el PDF y devolverlo
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.factura_id}.pdf"'
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
