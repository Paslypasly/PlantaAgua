# ventas/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from core.mixins import RolRequiredMixin
from .models import Pedido


class PedidoListView(RolRequiredMixin, ListView):
    model = Pedido
    template_name = "ventas/pedido_list.html"
    context_object_name = "pedidos"
    roles_permitidos = ["ADMIN", "OPERARIO", "GERENTE"]


class PedidoCreateView(RolRequiredMixin, CreateView):
    model = Pedido
    fields = ["cliente", "fecha", "estado", "monto_total"]
    template_name = "ventas/pedido_form.html"
    success_url = reverse_lazy("ventas_pedidos")
    roles_permitidos = ["ADMIN", "OPERARIO"]
