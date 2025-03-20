from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, F
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from .models import Factura
from pedidos.models import Pedido
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

@csrf_exempt
def generar_factura(request, pedido_id):
    """
    Genera una factura en PDF para un pedido específico.
    """
    if request.method == 'GET':
        try:
            pedido = Pedido.objects.get(id=pedido_id)

            # Calcular el total de la factura considerando cantidad * precio_unitario
            total_factura = pedido.items.aggregate(
                total=Sum(F('cantidad') * F('precio_unitario'))
            )['total'] or 0

            # Crear la factura
            factura = Factura.objects.create(
                pedido=pedido,
                total=total_factura
            )

            # Crear un buffer para el PDF
            buffer = io.BytesIO()

            # Crear el PDF con ReportLab
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 12)

            # Encabezado de la factura
            pdf.drawString(100, 750, f"Factura #{factura.factura_id}")
            pdf.drawString(100, 730, f"Fecha de emisión: {factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}") #año, mes // hora, minuto, segundo
            pdf.drawString(100, 710, f"Pedido #{pedido.id}")
            pdf.drawString(100, 690, f"Cliente: {pedido.usuario.username}")

            # Detalles de los ítems
            y = 650
            pdf.drawString(100, y, "Detalles del pedido:")
            y -= 20

            for item in pedido.items.all():
                total_producto = item.cantidad * item.precio_unitario
                pdf.drawString(120, y, f"{item.cantidad}x {item.producto.nombre} - ${item.precio_unitario} c/u (Total: ${total_producto})")
                y -= 20

            # Total de la factura
            pdf.drawString(100, y - 20, f"Total a pagar: ${total_factura}")

            # Finalizar el PDF
            pdf.showPage()
            pdf.save()

            # Devolver el PDF como respuesta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="factura_{factura.factura_id}.pdf"'
            return response
        except Pedido.DoesNotExist:
            return JsonResponse({'error': 'El pedido no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def listar_facturas(request):
    """
    Lista todas las facturas con filtros opcionales:
    - ?fecha=YYYY-MM-DD  (Filtra por fecha de emisión)
    - ?cliente=username   (Filtra por cliente)
    - ?pedido_id=123      (Filtra por pedido específico)
    """
    if request.method == 'GET':
        facturas = Factura.objects.all()

        # Aplicar filtros según los parámetros de la solicitud
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

        # Convertir a JSON
        facturas_data = [{
            'factura_id': factura.factura_id,
            'pedido_id': factura.pedido.id,
            'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d'),
            'cliente': factura.pedido.usuario.username,
            'total': str(factura.total)
        } for factura in facturas]

        return JsonResponse(facturas_data, safe=False)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def descargar_factura_pdf(request, factura_id):
    """
    Descarga una factura en formato PDF.
    """
    try:
        # Obtener la factura
        factura = Factura.objects.get(factura_id=factura_id)

        # Crear un buffer para el PDF
        buffer = io.BytesIO()

        # Crear el PDF con ReportLab
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        # Encabezado de la factura
        pdf.drawString(100, 750, f"Factura #{factura.factura_id}")
        pdf.drawString(100, 730, f"Fecha de emisión: {factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
        pdf.drawString(100, 710, f"Pedido #{factura.pedido.id}")
        pdf.drawString(100, 690, f"Cliente: {factura.pedido.usuario.username}")

        # Detalles de los ítems
        y = 650
        pdf.drawString(100, y, "Detalles del pedido:")
        y -= 20

        for item in factura.pedido.items.all():
            total_producto = item.cantidad * item.precio_unitario
            pdf.drawString(120, y, f"{item.cantidad}x {item.producto.nombre} - ${item.precio_unitario} c/u (Total: ${total_producto})")
            y -= 20

        # Total de la factura
        pdf.drawString(100, y - 20, f"Total a pagar: ${factura.total}")

        # Finalizar el PDF
        pdf.showPage()
        pdf.save()

        # Devolver el PDF como respuesta
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.factura_id}.pdf"'
        return response
    except Factura.DoesNotExist:
        return JsonResponse({'error': 'La factura no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)