# inventario/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from core.mixins import RolRequiredMixin
from .models import Insumo, MovimientoInventario


class InsumoListView(RolRequiredMixin, ListView):
    model = Insumo
    template_name = "inventario/insumo_list.html"
    context_object_name = "insumos"
    roles_permitidos = ["ADMIN", "OPERARIO", "GERENTE"]


class MovimientoInventarioListView(RolRequiredMixin, ListView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_list.html"
    context_object_name = "movimientos"
    roles_permitidos = ["ADMIN", "OPERARIO"]


class MovimientoInventarioCreateView(RolRequiredMixin, CreateView):
    model = MovimientoInventario
    fields = ["insumo", "tipo_movimiento", "cantidad", "motivo"]
    template_name = "inventario/movimiento_form.html"
    success_url = reverse_lazy("inventario_movimientos")
    roles_permitidos = ["ADMIN", "OPERARIO"]
