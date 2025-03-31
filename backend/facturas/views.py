from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Factura
from pedidos.models import Pedido
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from datetime import datetime

@csrf_exempt
def generar_factura(request, pedido_id):
    """
    Vista para generar una factura en PDF para un pedido específico.
    Incluye todos los datos del usuario y guarda el PDF en media/facturas.
    """
    if request.method == 'GET':
        try:
            # Obtener el pedido con el usuario relacionado (optimizado)
            pedido = Pedido.objects.select_related('usuario').get(id=pedido_id)
            usuario = pedido.usuario

            # Crear la factura (o obtener existente)
            factura, created = Factura.objects.get_or_create(
                pedido=pedido,
                defaults={'total': pedido.total}
            )

            # Crear buffer para el PDF
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 12)

            # --- Encabezado ---
            pdf.drawString(100, 800, "FACTURA")
            pdf.drawString(100, 780, f"Número: #{factura.id}")
            pdf.drawString(100, 760, f"Fecha: {factura.fecha_emision.strftime('%d/%m/%Y %H:%M')}")
            
            # --- Datos del cliente ---
            pdf.drawString(100, 730, "DATOS DEL CLIENTE:")
            pdf.drawString(120, 710, f"Nombre: {usuario.nombre_completo()}")
            pdf.drawString(120, 690, f"Cédula: {usuario.cedula}")
            pdf.drawString(120, 670, f"Dirección: {usuario.direccion or 'No registrada'}")
            pdf.drawString(120, 650, f"Teléfono: {str(usuario.telefono) if usuario.telefono else 'No registrado'}")
            pdf.drawString(120, 630, f"Email: {usuario.email}")

            # --- Detalles del pedido ---
            pdf.drawString(100, 600, "DETALLES DEL PEDIDO:")
            y = 580
            for item in pedido.items.all():
                pdf.drawString(120, y, f"• {item.cantidad}x {item.producto.nombre} - ${item.precio_unitario} c/u")
                y -= 20

            # --- Totales ---
            pdf.drawString(100, y - 40, f"Subtotal: ${factura.total}")
            pdf.drawString(100, y - 60, f"Total a pagar: ${factura.total}")
            pdf.drawString(100, y - 80, "¡Gracias por su compra!")

            pdf.showPage()
            pdf.save()

            # --- Guardar en media/facturas ---
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'facturas'), exist_ok=True)
            filename = f"factura_{factura.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(settings.MEDIA_ROOT, 'facturas', filename)
            
            with open(filepath, 'wb') as f:
                f.write(buffer.getvalue())

            # Devolver el PDF como respuesta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Pedido.DoesNotExist:
            return JsonResponse({'error': 'Pedido no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def listar_facturas(request):
    """
    Vista para listar todas las facturas con datos básicos del usuario.
    """
    if request.method == 'GET':
        facturas = Factura.objects.select_related('pedido__usuario').all()
        
        facturas_data = [{
            'id': factura.id,
            'pedido_id': factura.pedido.id,
            'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d %H:%M'),
            'total': str(factura.total),
            'cliente': {
                'nombre': factura.pedido.usuario.nombre_completo(),
                'cedula': factura.pedido.usuario.cedula,
                'email': factura.pedido.usuario.email
            }
        } for factura in facturas]
        
        return JsonResponse(facturas_data, safe=False)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)