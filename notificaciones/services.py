from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Notificacion

User = get_user_model()


def crear_notificacion(usuario, tipo: str, titulo: str, mensaje: str) -> Notificacion:
    """
    Crea una notificación para un usuario específico.
    """
    return Notificacion.objects.create(
        usuario=usuario,
        tipo=tipo,
        titulo=titulo,
        mensaje=mensaje,
    )


def crear_notificacion_para_roles(
    roles: list[str],
    tipo: str,
    titulo: str,
    mensaje: str,
) -> int:
    """
    Crea la misma notificación para todos los usuarios activos
    cuyo 'rol' esté en la lista de roles.
    Retorna cuántos usuarios fueron notificados.
    """
    usuarios = User.objects.filter(is_active=True, rol__in=roles)
    for usuario in usuarios:
        crear_notificacion(usuario, tipo, titulo, mensaje)
    return usuarios.count()


def marcar_notificaciones_como_leidas(usuario) -> int:
    """
    Marca todas las notificaciones no leídas del usuario como leídas.
    """
    qs = Notificacion.objects.filter(usuario=usuario, leida=False)
    ahora = timezone.now()
    count = qs.count()
    if count:
        qs.update(leida=True, fecha_leida=ahora)
    return count
