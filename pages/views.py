# pages/views.py
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(TemplateView):
    """
    Home básico del sistema. 
    Si quieres, después lo cambiamos para redirigir según rol.
    """
    template_name = "pages/home.html"


@method_decorator(login_required, name="dispatch")
class AcercaView(TemplateView):
    template_name = "pages/acerca.html"


@method_decorator(login_required, name="dispatch")
class SoporteView(TemplateView):
    template_name = "pages/soporte.html"


@method_decorator(login_required, name="dispatch")
class ContactoView(TemplateView):
    template_name = "pages/contacto.html"
