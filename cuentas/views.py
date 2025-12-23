# cuentas/views.py
from django.contrib import messages
from django.contrib import messages
from django.utils import timezone
from django.db import models  # ✅ <-- AGREGA ESTA LÍNEA
from produccion.models import LoteProduccion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm, PerfilUsuarioForm
from .mixins import RolRequiredMixin


# ===============================================================
#                    AUTENTICACIÓN PROFESIONAL
# ===============================================================

class CustomLoginView(LoginView):
    """
    Login del sistema (solo trabajadores).
    Redirige automáticamente según rol.
    """
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse_lazy("panel_admin")

        mapa = {
            Usuario.Rol.ADMIN: "panel_admin",
            Usuario.Rol.OPERARIO: "panel_operario",
            Usuario.Rol.CONDUCTOR: "panel_conductor",
            Usuario.Rol.GERENTE: "panel_gerente",
            Usuario.Rol.AUDITOR: "panel_admin",   # opcional
            Usuario.Rol.TECNICO: "panel_operario"
        }

        return reverse_lazy(mapa.get(user.rol, "panel_operario"))


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")


# ===============================================================
#                         PERFIL DEL USUARIO
# ===============================================================

class PerfilView(LoginRequiredMixin, UpdateView):
    """
    Perfil del usuario logueado.
    """
    model = Usuario
    form_class = PerfilUsuarioForm
    template_name = "cuentas/perfil.html"
    success_url = reverse_lazy("perfil")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)


# ===============================================================
#                  CRUD DE USUARIOS – SOLO ADMIN
# ===============================================================

class UsuarioListView(RolRequiredMixin, ListView):
    model = Usuario
    template_name = "cuentas/usuarios_list.html"
    context_object_name = "usuarios"
    rol_requerido = Usuario.Rol.ADMIN


class UsuarioCreateView(RolRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = "cuentas/usuario_form.html"
    success_url = reverse_lazy("usuarios_list")
    rol_requerido = Usuario.Rol.ADMIN

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado correctamente.")
        return super().form_valid(form)


class UsuarioUpdateView(RolRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioChangeForm
    template_name = "cuentas/usuario_form.html"
    success_url = reverse_lazy("usuarios_list")
    rol_requerido = Usuario.Rol.ADMIN

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)


class UsuarioDeleteView(RolRequiredMixin, DeleteView):
    model = Usuario
    template_name = "cuentas/usuario_confirm_delete.html"
    success_url = reverse_lazy("usuarios_list")
    rol_requerido = Usuario.Rol.ADMIN

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


# ===============================================================
#                     PANELES POR ROL
# ===============================================================

class PanelAdminView(LoginRequiredMixin, RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_admin.html"
    rol_requerido = Usuario.Rol.ADMIN

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from django.utils import timezone

        # -------- USUARIOS --------
        ctx["total_usuarios"] = Usuario.objects.count()

        # -------- CLIENTES --------
        try:
            from clientes.models import Cliente
            ctx["total_clientes"] = Cliente.objects.count()
        except Exception:
            ctx["total_clientes"] = 0

        # -------- SENSORES --------
        try:
            from sensores.models import Sensor
            ctx["sensores_activos"] = Sensor.objects.filter(activo=True).count()
            ctx["total_sensores"] = Sensor.objects.count()
        except Exception:
            ctx["sensores_activos"] = 0
            ctx["total_sensores"] = 0

        # -------- ACTUADORES --------
        try:
            from sensores.models import Actuador
            ctx["actuadores_on"] = Actuador.objects.filter(estado_on=True).count()
            ctx["total_actuadores"] = Actuador.objects.count()
        except Exception:
            ctx["actuadores_on"] = 0
            ctx["total_actuadores"] = 0

        # -------- ALERTAS --------
        try:
            from sensores.models import Alerta
            # solo alertas de sensores activos y no atendidas
            ctx["alertas_abiertas"] = Alerta.objects.filter(
                atendida=False,
                sensor__activo=True
            ).count()
            ctx["ultimas_alertas"] = Alerta.objects.filter(
                atendida=False,
                sensor__activo=True
            ).order_by("-created_at")[:5]
        except Exception:
            ctx["alertas_abiertas"] = 0
            ctx["ultimas_alertas"] = []

        # -------- LECTURAS RECIENTES --------
        try:
            from sensores.models import LecturaSensor
            ctx["lecturas_recientes"] = (
                LecturaSensor.objects.select_related("sensor")
                .order_by("-fecha_hora")[:5]
            )
        except Exception:
            ctx["lecturas_recientes"] = []

        ctx["hoy"] = timezone.localdate()
        return ctx




from django.utils import timezone
from produccion.models import LoteProduccion


class PanelOperarioView(LoginRequiredMixin, RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_operario.html"
    rol_requerido = Usuario.Rol.OPERARIO

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        hoy = timezone.localdate()

        # Obtener total de litros producidos hoy
        litros_hoy = (
            LoteProduccion.objects
            .filter(fecha=hoy)
            .aggregate(total=models.Sum("litros"))
            .get("total") or 0
        )

        # Si quieres mostrar también el número de lotes de hoy
        lotes_hoy = LoteProduccion.objects.filter(fecha=hoy).count()

        ctx["litros_hoy"] = litros_hoy
        ctx["lotes_hoy"] = lotes_hoy
        ctx["hoy"] = hoy

        return ctx



class PanelConductorView(LoginRequiredMixin, RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_conductor.html"
    rol_requerido = Usuario.Rol.CONDUCTOR


class PanelGerenteView(LoginRequiredMixin, RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_gerente.html"
    rol_requerido = Usuario.Rol.GERENTE


# ===============================================================
#          REDIRECT AUTOMÁTICO SEGÚN ROL (opcional)
# ===============================================================

def redirigir_por_rol(request):
    user = request.user
    mapa = {
        Usuario.Rol.ADMIN: "panel_admin",
        Usuario.Rol.OPERARIO: "panel_operario",
        Usuario.Rol.CONDUCTOR: "panel_conductor",
        Usuario.Rol.GERENTE: "panel_gerente",
    }
    return redirect(mapa.get(user.rol, "panel_operario"))
