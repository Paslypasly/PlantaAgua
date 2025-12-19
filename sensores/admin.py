# sensores/admin.py
from django.contrib import admin, messages
from .models import (
    TipoSensor,
    Sensor,
    LecturaSensor,
    Actuador,
    Alerta,
    ReglaControl,
    LecturaCrudaESP32,
)
from .services import forzar_actuador, activar_sensor


# ============================================================
# === TIPO DE SENSOR =========================================
# ============================================================

@admin.register(TipoSensor)
class TipoSensorAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "activo")
    search_fields = ("codigo", "descripcion")


# ============================================================
# === SENSORES ===============================================
# ============================================================

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "tipo",
        "estanque",
        "estado",
        "activo",
        "rango_min",
        "rango_max",
    )
    list_filter = ("tipo", "activo", "estado")
    search_fields = ("codigo",)
    list_editable = ("rango_min", "rango_max")  # permite ajustar directamente
    actions = ["activar_sensores", "desactivar_sensores"]

    @admin.action(description="Activar sensores seleccionados")
    def activar_sensores(self, request, queryset):
        for sensor in queryset:
            activar_sensor(sensor.id, True, request.user)
        self.message_user(
            request, f"Se activaron {queryset.count()} sensores correctamente.", messages.SUCCESS
        )

    @admin.action(description="Desactivar sensores seleccionados")
    def desactivar_sensores(self, request, queryset):
        for sensor in queryset:
            activar_sensor(sensor.id, False, request.user)
        self.message_user(
            request, f"Se desactivaron {queryset.count()} sensores correctamente.", messages.WARNING
        )


# ============================================================
# === LECTURAS ===============================================
# ============================================================

@admin.register(LecturaSensor)
class LecturaSensorAdmin(admin.ModelAdmin):
    list_display = ("sensor", "valor", "fecha_hora")
    list_filter = ("sensor", "fecha_hora")
    search_fields = ("sensor__codigo",)
    date_hierarchy = "fecha_hora"


# ============================================================
# === ACTUADORES =============================================
# ============================================================

@admin.register(Actuador)
class ActuadorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "estado_on", "descripcion")
    list_filter = ("tipo", "estado_on")
    search_fields = ("nombre", "descripcion")
    actions = ["forzar_encendido", "forzar_apagado"]

    @admin.action(description="Forzar encendido de actuadores seleccionados")
    def forzar_encendido(self, request, queryset):
        for act in queryset:
            forzar_actuador(act.id, True, request.user)
        self.message_user(
            request, f"Se forzaron {queryset.count()} actuadores a encendido (ON).", messages.SUCCESS
        )

    @admin.action(description="Forzar apagado de actuadores seleccionados")
    def forzar_apagado(self, request, queryset):
        for act in queryset:
            forzar_actuador(act.id, False, request.user)
        self.message_user(
            request, f"Se apagaron {queryset.count()} actuadores (OFF).", messages.WARNING
        )


# ============================================================
# === ALERTAS ================================================
# ============================================================

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("sensor", "severidad", "mensaje", "atendida", "created_at")
    list_filter = ("severidad", "atendida")
    search_fields = ("sensor__codigo", "mensaje")
    list_editable = ("atendida",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


# ============================================================
# === REGLAS DE CONTROL ======================================
# ============================================================

@admin.register(ReglaControl)
class ReglaControlAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sensor", "condicion", "umbral", "actuador")
    list_filter = ("sensor__tipo",)
    search_fields = ("nombre", "sensor__codigo")


# ============================================================
# === LECTURA CRUDA ESP32 ====================================
# ============================================================

@admin.register(LecturaCrudaESP32)
class LecturaCrudaESP32Admin(admin.ModelAdmin):
    list_display = ("sensor_id", "nivel_cm", "ir_estado", "ph", "timestamp")
    list_filter = ("sensor_id", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)
