from django.contrib import admin
from .models import Factura
from django.utils.html import format_html

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'fecha_emision', 'cliente_info', 'total', 'pdf_link')
    readonly_fields = ('numero_factura', 'pdf_preview')
    
    def cliente_info(self, obj):
        return obj.pedido.usuario.nombre_completo()
    cliente_info.short_description = 'Cliente'

    def pdf_link(self, obj):
        if obj.archivo_pdf:
            return format_html('<a href="{}">Descargar</a>', obj.archivo_pdf.url)
        return "-"
    pdf_link.short_description = 'PDF'