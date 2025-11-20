# core/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RolRequiredMixin(LoginRequiredMixin):
    """
    Mixin para vistas basadas en clases que valida que el usuario
    tenga alguno de los roles permitidos.
    Uso:
        class MiVista(RolRequiredMixin, ListView):
            roles_permitidos = ["ADMIN", "GERENTE"]
    """
    roles_permitidos: list[str] = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.roles_permitidos and request.user.rol not in self.roles_permitidos:
            raise PermissionDenied("No tiene permisos para acceder a esta vista.")

        return super().dispatch(request, *args, **kwargs)
