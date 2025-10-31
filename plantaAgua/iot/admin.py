from django.contrib import admin
from .models import Equipo, Sensor, EstacionLlenado

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("id", "planta", "tipo", "modelo", "ubicacion", "activo")
    list_filter = ("planta", "tipo", "activo")
    search_fields = ("modelo", "serie", "ubicacion")

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("id", "planta", "tipo", "unidad", "topico_mqtt", "rango_min", "rango_max", "activo")
    list_filter = ("planta", "tipo", "activo")
    search_fields = ("topico_mqtt",)
    autocomplete_fields = ("equipo",)

@admin.register(EstacionLlenado)
class EstacionLlenadoAdmin(admin.ModelAdmin):
    list_display = ("id", "planta", "nombre", "caudal_nominal_lpm")
    list_filter = ("planta",)
    search_fields = ("nombre",)
