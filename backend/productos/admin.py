from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible', 'categoria')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria', 'fecha_creacion')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_productos')
    prepopulated_fields = {'slug': ('nombre',)}