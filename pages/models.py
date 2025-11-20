# pages/models.py
from django.db import models
from core.models import BaseModel


class MensajeContacto(BaseModel):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()

    def __str__(self) -> str:
        return f"{self.asunto} - {self.nombre}"
