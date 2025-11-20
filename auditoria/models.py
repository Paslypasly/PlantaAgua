# auditoria/models.py
from django.db import models
from django.conf import settings
from core.models import BaseModel


class LogAcceso(BaseModel):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_acceso"
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    accion = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.usuario} - {self.accion} - {self.created_at}"


class LogEvento(BaseModel):
    modulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    severidad = models.CharField(
        max_length=20,
        blank=True,
        help_text="Ej. INFO, WARNING, ERROR, CRITICO."
    )

    def __str__(self) -> str:
        return f"{self.modulo} - {self.severidad}"
