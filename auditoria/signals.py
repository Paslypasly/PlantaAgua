from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import LogAcceso


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]
    LogAcceso.objects.create(
        usuario=user,
        ip=ip,
        user_agent=user_agent,
        accion="login",
    )


@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]
    LogAcceso.objects.create(
        usuario=user,
        ip=ip,
        user_agent=user_agent,
        accion="logout",
    )
