from django.contrib import admin
from .models import Categoria, Producto

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_cantidad_productos', 'activo', 'visible')
    readonly_fields = ('get_cantidad_productos',)
    search_fields = ('nombre',)
    
    @admin.display(description='Productos')
    def get_cantidad_productos(self, obj):
        return obj.productos.count()

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'get_disponible', 'categoria', 'activo')
    list_filter = ('categoria', 'activo', 'destacado')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('get_disponible', 'imagen_admin')
    
    @admin.display(description='Disponible')
    def get_disponible(self, obj):
        return obj.stock > 0
    
    @admin.display(description='Imagen')
    def imagen_admin(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" />', obj.imagen.url)
        return "Sin imagen"

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)