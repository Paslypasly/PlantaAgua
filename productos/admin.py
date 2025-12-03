from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaProducto, Producto


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "categoria",
        "presentacion_litros",
        "precio_lista",
        "activo",
        "preview",
    )
    list_filter = ("activo", "categoria")
    search_fields = ("nombre",)

    readonly_fields = ("preview",)

    def preview(self, obj):
        """Muestra una miniatura de la imagen en el admin."""
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:4px;">', obj.image.url)
        return "Sin imagen"
