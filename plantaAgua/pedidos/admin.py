from django.contrib import admin
from .models import Cliente, Pedido, PedidoItem, PedidoTracking

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1

class PedidoTrackingInline(admin.TabularInline):
    model = PedidoTracking
    extra = 0
    readonly_fields = ("estado", "timestamp", "nota", "lat", "lon")
    can_delete = False

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rut", "telefono")
    search_fields = ("nombre", "rut", "telefono")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "planta", "cliente", "estado", "total", "fecha", "actualizado")
    list_filter = ("planta", "estado", "fecha")
    search_fields = ("id", "cliente__nombre", "cliente__rut")
    inlines = [PedidoItemInline, PedidoTrackingInline]
    actions = ["marcar_recibido", "marcar_preparacion", "marcar_en_ruta", "marcar_entregado", "marcar_fallido"]

    def _push_tracking(self, queryset, estado, nota=None):
        created = 0
        for ped in queryset:
            if ped.estado != estado:
                ped.estado = estado
                ped.save(update_fields=["estado"])
                PedidoTracking.objects.create(pedido=ped, estado=estado, nota=nota or "")
                created += 1
        self.message_user(None, f"Actualizados {created} pedido(s) → {estado}")

    @admin.action(description="1) Marcar como RECIBIDO")
    def marcar_recibido(self, request, queryset):
        self._push_tracking(queryset, "RECIBIDO", "Pedido recibido")

    @admin.action(description="2) Marcar como PREPARACIÓN")
    def marcar_preparacion(self, request, queryset):
        self._push_tracking(queryset, "PREPARACION", "Pedido en preparación")

    @admin.action(description="3) Marcar como EN RUTA")
    def marcar_en_ruta(self, request, queryset):
        self._push_tracking(queryset, "EN_RUTA", "Pedido despachado")

    @admin.action(description="Marcar como ENTREGADO")
    def marcar_entregado(self, request, queryset):
        self._push_tracking(queryset, "ENTREGADO", "Pedido entregado")

    @admin.action(description="Marcar como FALLIDO")
    def marcar_fallido(self, request, queryset):
        self._push_tracking(queryset, "FALLIDO", "Entrega fallida / devuelto")

@admin.register(PedidoTracking)
class PedidoTrackingAdmin(admin.ModelAdmin):
    list_display = ("pedido", "estado", "timestamp", "lat", "lon", "nota")
    list_filter = ("estado", "timestamp")
    search_fields = ("pedido__id", "nota")
