# cuentas/views.py
from django.contrib import messages
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


class PanelOperarioView(LoginRequiredMixin, RolRequiredMixin, TemplateView):
    template_name = "cuentas/panel_operario.html"
    rol_requerido = Usuario.Rol.OPERARIO


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
