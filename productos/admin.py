# productos/admin.py
from django.contrib import admin
from .models import CategoriaProducto, Producto


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "presentacion_litros", "categoria", "precio_lista")
    list_filter = ("categoria",)
    search_fields = ("nombre",)
