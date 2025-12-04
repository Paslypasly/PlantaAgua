from django.contrib import admin
from .models import LogAcceso, LogEvento


@admin.register(LogAcceso)
class LogAccesoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "accion", "ip", "created_at")
    list_filter = ("accion", "usuario")
    search_fields = ("usuario__username", "ip", "accion")
    readonly_fields = ("usuario", "ip", "user_agent", "accion", "created_at")


@admin.register(LogEvento)
class LogEventoAdmin(admin.ModelAdmin):
    list_display = ("id", "modulo", "severidad", "created_at")
    list_filter = ("modulo", "severidad")
    search_fields = ("modulo", "descripcion", "severidad")
    readonly_fields = ("modulo", "descripcion", "severidad", "created_at")
