from django.contrib import admin
from .models import RutaDistribucion, RutaParada

class RutaParadaInline(admin.TabularInline):
    model = RutaParada
    extra = 0

@admin.register(RutaDistribucion)
class RutaDistribucionAdmin(admin.ModelAdmin):
    list_display = ("planta", "fecha", "chofer", "vehiculo", "estado")
    list_filter = ("planta", "estado", "fecha")
    search_fields = ("chofer", "vehiculo")
    inlines = [RutaParadaInline]

@admin.register(RutaParada)
class RutaParadaAdmin(admin.ModelAdmin):
    list_display = ("ruta", "orden", "pedido", "eta", "llegada", "salida", "estado")
    list_filter = ("estado",)
    search_fields = ("pedido__id",)
