# compras/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from core.mixins import RolRequiredMixin
from .models import OrdenCompra


class OrdenCompraListView(RolRequiredMixin, ListView):
    model = OrdenCompra
    template_name = "compras/ordencompra_list.html"
    context_object_name = "ordenes"
    roles_permitidos = ["ADMIN", "GERENTE"]


class OrdenCompraCreateView(RolRequiredMixin, CreateView):
    model = OrdenCompra
    fields = ["proveedor", "fecha", "estado", "monto_total"]
    template_name = "compras/ordencompra_form.html"
    success_url = reverse_lazy("compras_ordenes")
    roles_permitidos = ["ADMIN"]
