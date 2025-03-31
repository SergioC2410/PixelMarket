from django.contrib import admin
from .models import Factura
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_factura', 
        'fecha_emision_short', 
        'cliente_info', 
        'total_formateado',
        'pdf_link'
    )
    list_filter = ('fecha_emision',)
    search_fields = ('numero_factura', 'pedido__id')
    readonly_fields = ('numero_factura', 'pdf_preview')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_factura', 'pedido', 'total')
        }),
        ('Archivo PDF', {
            'fields': ('pdf_preview', 'archivo_pdf')
        }),
    )

    # Métodos personalizados
    def fecha_emision_short(self, obj):
        return obj.fecha_emision.strftime('%d/%m/%Y')
    fecha_emision_short.short_description = 'Fecha'

    def total_formateado(self, obj):
        return f"${obj.total:,.2f}"
    total_formateado.short_description = 'Total'

    def cliente_info(self, obj):
        return obj.pedido.usuario.nombre_completo()
    cliente_info.short_description = 'Cliente'

    def pdf_link(self, obj):
        if obj.archivo_pdf:
            return format_html(
                '<a href="{}" target="_blank">Descargar</a>',
                obj.archivo_pdf.url
            )
        return "-"
    pdf_link.short_description = 'PDF'

    def pdf_preview(self, obj):
        if obj.archivo_pdf:
            return format_html(
                '<embed src="{}" width="400" height="300" type="application/pdf">',
                obj.archivo_pdf.url
            )
        return "PDF no generado"
    pdf_preview.short_description = 'Vista Previa'