# core/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RolRequiredMixin(LoginRequiredMixin):
    """
    Mixin para vistas que requieren que el usuario tenga cierto rol.
    - Si no está autenticado -> redirige a login.
    - Si es superuser -> siempre pasa.
    - Si su rol no está en roles_permitidos -> 403.
    """
    roles_permitidos = []

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return self.handle_no_permission()

        # superusuario siempre puede entrar
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.roles_permitidos and user.rol not in self.roles_permitidos:
            raise PermissionDenied("No tienes permiso para ver esta vista.")

        return super().dispatch(request, *args, **kwargs)
