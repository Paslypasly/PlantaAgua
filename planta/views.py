# planta/views.py
from django.views.generic import TemplateView
from core.mixins import RolRequiredMixin
from .services import obtener_resumen_planta


class DashboardPlantaView(RolRequiredMixin, TemplateView):
    template_name = "planta/dashboard_planta.html"
    roles_permitidos = ["ADMIN", "OPERARIO", "GERENTE"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        resumen = obtener_resumen_planta()
        ctx.update(resumen)
        return ctx
