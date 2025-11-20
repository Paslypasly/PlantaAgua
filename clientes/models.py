# clientes/models.py
from django.db import models
from core.models import BaseModel, EntidadConRut


class SectorEntrega(BaseModel):
    nombre = models.CharField(max_length=50)
    recargo_delivery = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Recargo adicional por delivery asociado a este sector."
    )

    def __str__(self) -> str:
        return self.nombre


class Cliente(EntidadConRut):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    sector_entrega = models.ForeignKey(
        SectorEntrega,
        on_delete=models.PROTECT,
        related_name="clientes"
    )

    def __str__(self) -> str:
        return f"{self.nombre} ({self.rut_completo})"
