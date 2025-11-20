# core/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RolRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para exigir login + rol específico.
    Si rol_requerido = None, solo exige estar autenticado.
    """

    rol_requerido = None  # Ej: "ADMIN", "OPERARIO", etc.

    def test_func(self):
        user = self.request.user

        # Si no hay rol requerido, basta con que esté logueado
        if self.rol_requerido is None:
            return user.is_authenticated

        # Súper usuario siempre tiene acceso
        if user.is_superuser:
            return True

        # Comparamos contra el campo rol del modelo Usuario
        return getattr(user, "rol", None) == self.rol_requerido

    def handle_no_permission(self):
        """
        Si el usuario no tiene el rol adecuado, lanzamos 403.
        """
        if not self.request.user.is_authenticated:
            # Deja que LoginRequiredMixin redirija a login
            return super().handle_no_permission()

        # Usuario autenticado pero sin permiso → 403
        raise PermissionDenied("No tiene permiso para acceder a esta vista.")
