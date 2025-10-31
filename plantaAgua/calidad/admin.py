from django.contrib import admin
from .models import Lote, Medicion, Alarma, AlarmaLog, ChecklistPH

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ("codigo", "planta", "estacion", "operador", "estado", "fecha", "volumen_real_l", "tds", "uvi", "orp")
    list_filter = ("planta", "estado", "estacion")
    search_fields = ("codigo", "operador__username")

@admin.register(Medicion)
class MedicionAdmin(admin.ModelAdmin):
    list_display = ("planta", "sensor", "valor", "unidad", "timestamp", "calidad_ok", "lote")
    list_filter = ("planta", "sensor__tipo", "calidad_ok")
    search_fields = ("sensor__topico_mqtt",)

@admin.register(Alarma)
class AlarmaAdmin(admin.ModelAdmin):
    list_display = ("planta", "regla", "condicion", "umbral", "severidad", "activa")
    list_filter = ("planta", "severidad", "activa")
    search_fields = ("regla",)

@admin.register(AlarmaLog)
class AlarmaLogAdmin(admin.ModelAdmin):
    list_display = ("alarma", "planta", "sensor", "valor", "timestamp", "estado")
    list_filter = ("planta", "estado", "alarma__severidad")
    search_fields = ("alarma__regla", "sensor__topico_mqtt")

@admin.register(ChecklistPH)
class ChecklistPHAdmin(admin.ModelAdmin):
    list_display = ("planta", "fecha", "valor_ph", "firmado_por")
    list_filter = ("planta", "fecha")
    search_fields = ("firmado_por__username",)
