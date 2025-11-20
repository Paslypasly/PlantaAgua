from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rut_numero", "rut_dv", "email", "activo")
    search_fields = ("nombre", "rut_numero", "email")
