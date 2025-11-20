# cuentas/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from core.utils import rut as rut_utils


class Usuario(AbstractUser):
    """
    Usuario del sistema con rol de negocio y RUT.
    El DV se calcula automáticamente a partir del rut_numero.
    """

    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        OPERARIO = "OPERARIO", "Operario"
        CONDUCTOR = "CONDUCTOR", "Conductor"
        GERENTE = "GERENTE", "Gerente"
        TECNICO = "TECNICO", "Técnico"
        AUDITOR = "AUDITOR", "Auditor"

    # Mantengo ROL_CHOICES por si lo usas en otros lados
    ROL_CHOICES = Rol.choices

    rut_numero = models.CharField(
        max_length=8,
        verbose_name="RUT (sin DV)",
        blank=True,
        null=True,
        help_text="Solo números, sin puntos ni guion."
    )
    rut_dv = models.CharField(
        max_length=1,
        verbose_name="DV",
        blank=True,
        null=True
    )
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default=Rol.OPERARIO,
    )

    def get_rut_completo(self) -> str:
        if not self.rut_numero or not self.rut_dv:
            return ""
        return f"{self.rut_numero}-{self.rut_dv}"

    @property
    def rut_completo(self) -> str:
        return self.get_rut_completo()

    def clean(self):
        super().clean()
        if self.rut_numero:
            rut_num = rut_utils.normalizar_rut_numero(self.rut_numero)
            if len(rut_num) not in (7, 8):
                raise ValueError("El RUT debe tener 7 u 8 dígitos (sin DV).")
            self.rut_numero = rut_num
            self.rut_dv = rut_utils.calcular_dv(self.rut_numero)

    def save(self, *args, **kwargs):
        if self.rut_numero:
            rut_num = rut_utils.normalizar_rut_numero(self.rut_numero)
            self.rut_numero = rut_num
            self.rut_dv = rut_utils.calcular_dv(self.rut_numero)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.username} ({self.get_rol_display()})"
