# clientes/views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from core.mixins import RolRequiredMixin
from .models import Cliente

# clientes/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Cliente
from .forms import ClienteForm

class RegistroClienteView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/registro_cliente.html"
    success_url = reverse_lazy("home")  # o a una página de "gracias"

class ClienteListView(RolRequiredMixin, ListView):
    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"
    roles_permitidos = ["ADMIN", "OPERARIO", "GERENTE"]


class ClienteCreateView(RolRequiredMixin, CreateView):
    model = Cliente
    fields = ["nombre", "rut_numero", "rut_dv", "direccion", "telefono", "email", "activo"]
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes_lista")
    roles_permitidos = ["ADMIN", "OPERARIO"]
