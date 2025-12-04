from django.http import HttpRequest

from .models import LogAcceso, LogEvento


def registrar_acceso(request: HttpRequest, accion: str) -> LogAcceso:
    """
    Registra un acceso o acción de un usuario (login, logout, etc.).
    """
    usuario = request.user if request.user.is_authenticated else None
    ip = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]

    return LogAcceso.objects.create(
        usuario=usuario,
        ip=ip,
        user_agent=user_agent,
        accion=accion,
    )


def registrar_evento(modulo: str, descripcion: str, severidad: str = "INFO") -> LogEvento:
    """
    Registra un evento relevante de negocio o del sistema.
    """
    return LogEvento.objects.create(
        modulo=modulo,
        descripcion=descripcion,
        severidad=severidad,
    )
