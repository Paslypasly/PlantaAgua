# core/decorators.py
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def rol_requerido(*roles_permitidos):
    """
    Decorador para vistas basadas en función.
    Ej:
        @rol_requerido("ADMIN", "GERENTE")
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if roles_permitidos and request.user.rol not in roles_permitidos:
                raise PermissionDenied("No tiene permisos para acceder.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
