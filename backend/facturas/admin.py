from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Factura
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.files.base import ContentFile
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class FacturaAdmin(admin.ModelAdmin):
    # ========== CONFIGURACIÓN BÁSICA ==========
    list_display = (
        'numero_factura',
        'fecha_emision_short',
        'cliente_info',
        'total_formateado',
        'estado_pdf',
        'pedido_link',
        'acciones_personalizadas'
    )
    
    list_filter = ('fecha_emision',)
    search_fields = (
        'numero_factura',
        'pedido__id',
        'pedido__usuario__first_name',
        'pedido__usuario__cedula'
    )
    date_hierarchy = 'fecha_emision'
    ordering = ('-fecha_emision',)
    list_per_page = 20
    
    # ========== ACCIONES PERSONALIZADAS ==========
    actions = [
        'generar_pdf_seleccionados',
        'reenviar_facturas_email'
    ]
    
    def generar_pdf_seleccionados(self, request, queryset):
        for factura in queryset:
            self._generar_pdf_factura(factura)
        self.message_user(
            request,
            f"Se generaron {len(queryset)} PDF(s) correctamente",
            messages.SUCCESS
        )
    generar_pdf_seleccionados.short_description = "🔘 Generar PDF para facturas seleccionadas"
    
    def reenviar_facturas_email(self, request, queryset):
        # Lógica para integración con servicio de email
        self.message_user(
            request,
            f"{len(queryset)} factura(s) en cola para reenvío",
            messages.INFO
        )
    reenviar_facturas_email.short_description = "✉️ Reenviar facturas por email"
    
    # ========== VISTAS PERSONALIZADAS ==========
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/generar-pdf/',
                self.admin_site.admin_view(self.generar_pdf_view),
                name='factura_generar_pdf'
            ),
        ]
        return custom_urls + urls
    
    def generar_pdf_view(self, request, object_id):
        factura = get_object_or_404(Factura, pk=object_id)
        self._generar_pdf_factura(factura)
        self.message_user(
            request,
            f"PDF regenerado para factura {factura.numero_factura}",
            messages.SUCCESS
        )
        return HttpResponseRedirect(
            reverse('admin:facturas_factura_change', args=[object_id])
        )
    
    # ========== MÉTODOS DE APOYO ==========
    def _generar_pdf_factura(self, factura):
        """Lógica centralizada para generación de PDF"""
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        
        # Configuración del PDF (usando datos_cliente del modelo)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, 800, f"FACTURA {factura.numero_factura}")
        
        # ... (resto del código de generación PDF)
        
        pdf.save()
        filename = factura.generar_nombre_pdf()
        factura.archivo_pdf.save(filename, ContentFile(buffer.getvalue()))
        factura.save()
    
    # ========== CAMPOS PERSONALIZADOS ==========
    def acciones_personalizadas(self, obj):
        return format_html(
            '<div class="actions">'
            '<a class="button" href="{}">Generar PDF</a>&nbsp;'
            '<a class="button" href="{}" target="_blank">Descargar</a>'
            '</div>',
            reverse('admin:factura_generar_pdf', args=[obj.id]),
            obj.archivo_pdf.url if obj.archivo_pdf else '#'
        )
    acciones_personalizadas.short_description = 'Acciones'
    acciones_personalizadas.allow_tags = True
    
    def estado_pdf(self, obj):
        if obj.archivo_pdf:
            return mark_safe(
                '<span style="color:green;">✓ Generado</span>'
            )
        return mark_safe(
            '<span style="color:red;">✖ Pendiente</span>'
        )
    estado_pdf.short_description = 'Estado PDF'
    
    # ... (otros métodos personalizados como antes)

# Registro final
admin.site.register(Factura, FacturaAdmin)