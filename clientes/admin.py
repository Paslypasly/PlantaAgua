# clientes/admin.py
from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Soporta ambos escenarios:
    - Si tu EntidadConRut define campos: rut y dv
    - y tú antes querías rut_numero / rut_dv
    """

    list_display = ("nombre", "rut_numero", "rut_dv", "email", "activo")
    search_fields = ("nombre", "rut", "email")
    list_filter = ("activo",)

    @admin.display(description="RUT")
    def rut_numero(self, obj: Cliente):
        # EntidadConRut normalmente usa 'rut'
        return getattr(obj, "rut", "") or ""

    @admin.display(description="DV")
    def rut_dv(self, obj: Cliente):
        # EntidadConRut normalmente usa 'dv'
        return getattr(obj, "dv", "") or ""
