from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "tipo", "titulo", "leida")
    list_filter = ("tipo", "leida")
    search_fields = ("titulo", "mensaje", "usuario__username")
    readonly_fields = ("usuario", "tipo", "titulo", "mensaje", "fecha_leida")
