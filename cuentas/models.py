# cuentas/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Usuario del sistema con rol de negocio.
    Usaremos este modelo como AUTH_USER_MODEL.
    """
    ROL_CHOICES = [
        ("ADMIN", "Administrador"),
        ("OPERARIO", "Operario"),
        ("CONDUCTOR", "Conductor"),
        ("GERENTE", "Gerente"),
        ("TECNICO", "Técnico"),
        ("AUDITOR", "Auditor"),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default="OPERARIO"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return f"{self.username} ({self.get_rol_display()})"
