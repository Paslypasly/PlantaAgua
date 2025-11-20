from django.contrib import admin
from .models import TipoSensor, Sensor, LecturaSensor, Actuador, Alerta, ReglaControl


@admin.register(TipoSensor)
class TipoSensorAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "activo")


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("codigo", "tipo", "estanque", "activo", "estado")
    list_filter = ("tipo", "activo", "estado")


@admin.register(LecturaSensor)
class LecturaSensorAdmin(admin.ModelAdmin):
    list_display = ("sensor", "valor", "fecha_hora")
    list_filter = ("sensor",)


@admin.register(Actuador)
class ActuadorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "estado_on")


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("sensor", "severidad", "mensaje", "atendida", "created_at")
    list_filter = ("severidad", "atendida")


@admin.register(ReglaControl)
class ReglaControlAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sensor", "condicion", "umbral", "actuador")
