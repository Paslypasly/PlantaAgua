# cuentas/views.py
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core.mixins import RolRequiredMixin


class PanelAdminView(RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_admin.html"
    roles_permitidos = ["ADMIN"]


class PanelOperarioView(RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_operario.html"
    roles_permitidos = ["OPERARIO", "ADMIN"]


class PanelConductorView(RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_conductor.html"
    roles_permitidos = ["CONDUCTOR", "ADMIN"]


class PanelGerenteView(RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_gerente.html"
    roles_permitidos = ["GERENTE", "ADMIN"]


@login_required
def redirigir_por_rol(request):
    """
    Redirige al panel correcto según el rol del usuario.
    Ideal para usar como LOGIN_REDIRECT_URL.
    """
    user = request.user
    mapa = {
        "ADMIN": "panel_admin",
        "OPERARIO": "panel_operario",
        "CONDUCTOR": "panel_conductor",
        "GERENTE": "panel_gerente",
    }
    nombre_url = mapa.get(user.rol, "panel_operario")
    return redirect(nombre_url)
