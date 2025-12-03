from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AyudaView(TemplateView):
    template_name = "pages/ayuda.html"


class ContactoView(TemplateView):
    template_name = "pages/contacto.html"


class AcercaView(TemplateView):
    template_name = "pages/acerca.html"


class SoporteView(TemplateView):
    template_name = "pages/soporte.html"
