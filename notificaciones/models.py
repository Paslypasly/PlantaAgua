# notificaciones/models.py
from django.db import models
from django.conf import settings
from core.models import BaseModel


class Notificacion(BaseModel):
    TIPO_CHOICES = [
        ("ALERTA", "Alerta de sensor / planta"),
        ("MANTENCION", "Aviso de mantención"),
        ("STOCK", "Alerta de stock"),
        ("SISTEMA", "Notificación de sistema"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones"
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_leida = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.titulo} ({self.get_tipo_display()})"
