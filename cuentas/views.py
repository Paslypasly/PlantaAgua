# cuentas/views.py
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core.mixins import RolRequiredMixin
# cuentas/views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Usuario
from .forms import RegistroUsuarioForm, PerfilUsuarioForm
from .mixins import RolRequiredMixin  # si ya lo tienes, lo reutilizamos
# cuentas/views.py
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm
from .mixins import RolRequiredMixin  # el que ya usas en PanelAdminView


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


class CustomLoginView(LoginView):
    """
    Login usando el usuario personalizado.
    Usa autenticación estándar de Django, y redirige según rol.
    """
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user
        # Súper usuario siempre al panel admin
        if user.is_superuser:
            return reverse_lazy("panel_admin")

        if user.rol == Usuario.Rol.ADMIN:
            return reverse_lazy("panel_admin")
        elif user.rol == Usuario.Rol.OPERARIO:
            return reverse_lazy("panel_operario")
        elif user.rol == Usuario.Rol.CONDUCTOR:
            return reverse_lazy("panel_conductor")
        elif user.rol == Usuario.Rol.GERENTE:
            return reverse_lazy("panel_gerente")
        else:
            # fallback genérico
            return reverse_lazy("home")


class RegistroUsuarioView(CreateView):
    """
    Registro básico de usuario (para demo o para creación desde admin web).
    """
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = "cuentas/registro.html"
    success_url = reverse_lazy("login")


class PerfilView(LoginRequiredMixin, UpdateView):
    """
    Vista de perfil del usuario logueado.
    Permite actualizar email y ver RUT y rol.
    """
    model = Usuario
    form_class = PerfilUsuarioForm
    template_name = "cuentas/perfil.html"
    success_url = reverse_lazy("perfil")

    def get_object(self, queryset=None):
        # siempre el usuario actual
        return self.request.user


# ===================== PANELES POR ROL =====================

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
