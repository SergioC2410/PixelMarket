from django.contrib import admin
from .models import Factura
from django.utils.html import format_html

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_factura',
        'fecha_corta',
        'cliente_info',
        'total_formateado',
        'pdf_link'
    )
    readonly_fields = ('pdf_preview',)
    
    def fecha_corta(self, obj):
        return obj.fecha_emision.strftime('%d/%m/%Y')
    fecha_corta.short_description = 'Fecha'
    
    def cliente_info(self, obj):
        return obj.pedido.usuario.get_full_name()
    cliente_info.short_description = 'Cliente'
    
    def total_formateado(self, obj):
        return f"${obj.total:,.2f}"
    total_formateado.short_description = 'Total'
    
    def pdf_link(self, obj):
        if obj.archivo_pdf:
            return format_html(
                '<a href="{}" target="_blank">📄 Descargar</a>',
                obj.archivo_pdf.url
            )
        return "-"
    pdf_link.short_description = 'PDF'
    
    def pdf_preview(self, obj):
        if obj.archivo_pdf:
            return format_html(
                '<iframe src="{}" width="400" height="300"></iframe>',
                obj.archivo_pdf.url
            )
        return "PDF no generado"
    pdf_preview.short_description = 'Vista Previa'