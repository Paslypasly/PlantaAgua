# proveedores/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from core.mixins import RolRequiredMixin
from .models import Proveedor


class ProveedorListView(RolRequiredMixin, ListView):
    model = Proveedor
    template_name = "proveedores/proveedor_list.html"
    context_object_name = "proveedores"
    roles_permitidos = ["ADMIN", "GERENTE"]


class ProveedorCreateView(RolRequiredMixin, CreateView):
    model = Proveedor
    fields = ["nombre", "rut_numero", "rut_dv", "email", "telefono", "direccion", "activo"]
    template_name = "proveedores/proveedor_form.html"
    success_url = reverse_lazy("proveedores_lista")
    roles_permitidos = ["ADMIN"]
