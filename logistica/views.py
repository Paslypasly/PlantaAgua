# logistica/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from core.mixins import RolRequiredMixin
from .models import RutaEntrega


class RutaEntregaListView(RolRequiredMixin, ListView):
    model = RutaEntrega
    template_name = "logistica/ruta_list.html"
    context_object_name = "rutas"
    roles_permitidos = ["ADMIN", "CONDUCTOR", "OPERARIO", "GERENTE"]


class RutaEntregaCreateView(RolRequiredMixin, CreateView):
    model = RutaEntrega
    fields = ["fecha", "vehiculo", "conductor", "descripcion"]
    template_name = "logistica/ruta_form.html"
    success_url = reverse_lazy("logistica_rutas")
    roles_permitidos = ["ADMIN", "OPERARIO"]
