# planta/admin.py
from django.contrib import admin
from .models import Estanque, EventoPlanta, InventarioBidones


@admin.register(Estanque)
class EstanqueAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "capacidad_litros", "nivel_agua", "estado", "ph_actual", "updated_at")
    search_fields = ("nombre",)
    list_filter = ("tipo", "estado")


@admin.register(EventoPlanta)
class EventoPlantaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "created_at")
    search_fields = ("titulo",)
    ordering = ("-created_at",)


@admin.register(InventarioBidones)
class InventarioBidonesAdmin(admin.ModelAdmin):
    list_display = ("stock_10", "stock_20", "modo_pendiente", "tipo_pendiente", "ultimo_contador_esp", "ultima_accion", "updated_at")
    list_filter = ("modo_pendiente", "tipo_pendiente")
