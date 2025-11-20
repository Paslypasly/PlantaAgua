# cuentas/mixins.py
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin

class RolRequiredMixin(UserPassesTestMixin):
    rol_requerido = None

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if self.rol_requerido is None:
            return True
        return getattr(user, "rol", None) == self.rol_requerido

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied()
        return super().handle_no_permission()
