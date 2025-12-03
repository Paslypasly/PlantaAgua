from django.contrib import admin
from .models import Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ("subtotal",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "numero",
        "cliente",
        "fecha",
        "estado",
        "origen",
        "forma_pago",
        "total",
    )
    list_filter = ("estado", "origen", "forma_pago", "fecha")
    search_fields = ("numero", "cliente__nombre", "cliente__rut_numero")
    inlines = [DetallePedidoInline]
