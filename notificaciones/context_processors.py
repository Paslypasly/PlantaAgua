from .models import Notificacion


def notificaciones_no_leidas(request):
    """
    Expone en los templates la cantidad de notificaciones no leídas
    del usuario autenticado.
    """
    if not request.user.is_authenticated:
        return {}
    count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
    return {"notificaciones_no_leidas": count}
