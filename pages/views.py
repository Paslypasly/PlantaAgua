# pages/views.py
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import ContactoForm


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AcercaView(TemplateView):
    template_name = "pages/acerca.html"


class AyudaView(TemplateView):
    template_name = "pages/ayuda.html"


class ContactoView(FormView):
    """
    Página de contacto para clientes.
    GET  -> muestra el formulario
    POST -> valida y muestra mensaje de éxito
    """
    template_name = "pages/contacto.html"
    form_class = ContactoForm
    success_url = reverse_lazy("pages:contacto")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Hemos recibido tu mensaje. Nos pondremos en contacto contigo a la brevedad."
        )
        return super().form_valid(form)


class SoporteView(TemplateView):
    template_name = "pages/soporte.html"
