# proveedores/models.py
from django.db import models
from core.models import EntidadConRut


class Proveedor(EntidadConRut):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    contacto = models.CharField(
        max_length=120,
        blank=True,
        help_text="Nombre de la persona de contacto principal."
    )

    def __str__(self) -> str:
        return f"{self.nombre} ({self.rut_completo})"
